""" Create a mnemonic for testing GreenAddress """
from os import urandom
from wallycore import bip39_get_wordlist, bip39_mnemonic_from_bytes, \
        BIP39_ENTROPY_LEN_256


if __name__ == "__main__":

    # Only english wordlists are supported by GreenAddress wallets
    wordlist = bip39_get_wordlist('en')
    entropy = urandom(BIP39_ENTROPY_LEN_256)
    mnemonic = bip39_mnemonic_from_bytes(wordlist, entropy)
    print(mnemonic)
