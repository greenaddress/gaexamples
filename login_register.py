""" Example of registering a new wallet with GreenAddress """
from gacommon.utils import *
import sys


if __name__ == "__main__":

    mnemonics = sys.argv[1]

    conn = GAConnection(GAConnection.REGTEST_URI)

    # Convert our mnemonics into an HD wallet
    wallet = wallet_from_mnemonic(mnemonics)

    # We give the service our master pubkey and chaincode so that
    # it can derive and monitor addresses for us. Note that we
    # never expose our mnemonics or our private keys.
    master_pubkey = bip32_key_get_pub_key(wallet)
    master_chaincode = bip32_key_get_chain_code(wallet)

    # We derive a unique path from our wallet so that the service signs
    # our transactions with unique keys for our user.
    ga_path = derive_ga_path(wallet)

    # Finally we register the user
    ret = conn.call('login.register', h(master_pubkey), h(master_chaincode),
                    GAConnection.USER_AGENT, h(ga_path))

    # The call returns true when it succeeds
    print(ret)
