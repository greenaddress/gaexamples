from autobahn_sync import AutobahnSync
from autobahn.twisted.websocket import WampWebSocketClientFactory
import logging
import six
from time import sleep
from wallycore import *


logging.basicConfig(level=logging.ERROR)


# This hack is required to override the WAMP timeout:
_unpatched_setProtocolOptions = WampWebSocketClientFactory.setProtocolOptions


def _patched_setProtocolOptions(*args, **kwargs):
    kwargs['autoPingTimeout'] = 30 # Increase timeout
    return _unpatched_setProtocolOptions(*args, **kwargs)


WampWebSocketClientFactory.setProtocolOptions = _patched_setProtocolOptions

if six.PY3:
    def unicode(s):
        return s

class GAConnection(object):
    """ A class encapsulating a connection to the GreenAddress service """

    MAINNET_URI = u'wss://prodwss.greenaddress.it/v2/ws/'
    TESTNET_URI = u'wss://testwss.greenaddress.it/v2/ws/'
    REGTEST_URI = u'wss://regtestwss.greenaddress.it/v2/ws/'
    USER_AGENT = u'[v2,sw]gaexamples'
    TIMEOUT_SECONDS = 30

    def __init__(self, uri=None):
        """ Create a connection to the GreenAddress service """
        self.wamp = AutobahnSync()
        exc = None
        for attempt in range(self.TIMEOUT_SECONDS):
            try:
                self.wamp.run(url=uri or self.REGTEST_URI)
                return
            except Exception as e:
                exc = e
                sleep(1)
        raise exc

    def call(self, name, *args):
        """ Make an API call to the GreenAddress service """
        return self.wamp.session.call(u'com.greenaddress.' + unicode(name), *args)


def h(b):
    """ Convert bytes into a hex string """
    return hex_from_bytes(b)


def wallet_from_mnemonic(mnemonic):
    """ Generate a BIP32 HD Master Key (wallet) from a mnemonic phrase """
    bip39_mnemonic_validate(None, mnemonic)
    written, seed = bip39_mnemonic_to_seed512(mnemonic, None)
    assert written == BIP39_SEED_LEN_512
    return bip32_key_from_seed(seed, BIP32_VER_MAIN_PRIVATE,
                               BIP32_FLAG_SKIP_HASH)

def derive_ga_path(wallet):
    """ Derive the GreenAddress path from our wallet """
    # Note that the method of deriving the path has changed over time.
    # You should use this method only for registering new accounts.
    # The server returns your path to you when you login and and you
    # should use that returned path to derive addresses and sign.
    GA_KEY = '477265656e416464726573732e69742048442077616c6c65742070617468'
    GA_PATH_ROOT = [0x80000000 | 0x4741]
    flags = BIP32_FLAG_KEY_PUBLIC | BIP32_FLAG_SKIP_HASH
    hdkey = bip32_key_from_parent_path(wallet, GA_PATH_ROOT, flags)
    data = bip32_key_get_chain_code(hdkey) + bip32_key_get_pub_key(hdkey)
    return hmac_sha512(hex_to_bytes(GA_KEY), data)


def create_p2pkh_address(pubkey, testnet=False):
    """ Create a p2pkh address from a pubkey """
    version = b'\x6f' if testnet else b'\x00'
    pubkey_hash = bytes(hash160(pubkey))
    return base58check_from_bytes(version + pubkey_hash)


def _sign_login_challenge(wallet, challenge):
    """ Sign the challenge presented to us for logging in """
    # Convert the challenge into a bitcoin message hash
    message = bytearray('greenaddress.it      login ' + challenge, 'ascii')
    hash_ = format_bitcoin_message(message, BITCOIN_MESSAGE_FLAG_HASH)

    # Sign it using the signing key derived from the wallet
    flags = BIP32_FLAG_KEY_PRIVATE | BIP32_FLAG_SKIP_HASH
    login_key = bip32_key_from_parent_path(wallet, [0x4741b11e], flags)
    login_priv_key = bip32_key_get_priv_key(login_key)
    sig = ec_sig_from_bytes(login_priv_key, hash_, EC_FLAG_ECDSA)

    # Return the signature in DER encoding
    return ec_sig_to_der(sig)


def login(wallet, conn, testnet=False):
    """Log in a user"""
    # Create a p2pkh address from our master pubkey.
    master_pubkey = bip32_key_get_pub_key(wallet)
    p2pkh = create_p2pkh_address(master_pubkey, testnet)

    # Ask the server for a challenge to sign and sign it
    challenge = conn.call('login.get_trezor_challenge', p2pkh, True)
    sig = _sign_login_challenge(wallet, challenge)

    # Authenticate using the signed challenge
    # This returns the users login data or false if login fails
    return conn.call('login.authenticate', h(sig), False, 'GA',
                     'fake_device_id', GAConnection.USER_AGENT)
