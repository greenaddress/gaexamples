""" Example of authenticating (logging in) a user with GreenAddress """
from gacommon.utils import *
import sys

def do_login(mnemonic):
    conn = GAConnection(GAConnection.REGTEST_URI)

    # Convert our mnemonic into an HD wallet
    wallet = wallet_from_mnemonic(mnemonic)

    # Login the user. See gacommon/utils.py for the implementation
    return conn, wallet, login(wallet, conn, testnet=True)


if __name__ == "__main__":

    mnemonic = sys.argv[1]

    conn, wallet, login_data = do_login(mnemonic)

    print(login_data)
