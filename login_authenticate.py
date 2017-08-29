""" Example of authenticating (logging in) a user with GreenAddress """
from gacommon.utils import *
import sys

def do_login(mnemonics):
    conn = GAConnection(GAConnection.REGTEST_URI)

    # Convert our mnemonics into an HD wallet
    wallet = wallet_from_mnemonic(mnemonics)

    # Login the user. See gacommon/utils.py for the implementation
    return conn, wallet, login(wallet, conn, testnet=True)


if __name__ == "__main__":

    mnemonics = sys.argv[1]

    conn, wallet, login_data = do_login(mnemonics)

    print(login_data)
