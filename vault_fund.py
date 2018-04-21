""" Example of fetching a wallet receive address with GreenAddress """
from gacommon.utils import *
from login_authenticate import do_login
import sys


if __name__ == "__main__":

    mnemonic = sys.argv[1]

    # First, login a full user to fetch the address.
    # A watch only user can instead be used for funding so that you don't
    # need to use your mnemonic to fetch addresses for your wallet, e.g.
    # if you are a service receiving funds watch only is safer.
    conn, wallet, login_data = do_login(mnemonic)

    # Fetch the new address from the service
    subaccount = 0        # Main account
    return_pointer = True # Ask for the derivation pointer also
    addr_type = 'p2sh'    # Can also be p2wsh for a segwit address
    address = conn.call('vault.fund', subaccount, return_pointer, addr_type)

    # The returned information includes the derivation details and the
    # redeem script of the scriptSig.
    # For 2of2 accounts this is:
    #     OP_2 ga_pubkey user_pubkey OP_2 OP_CHECKMULTISIG
    # For 2of3 accounts it is:
    #     OP_2 ga_pubkey user_pubkey user_backup_pubkey OP_3 OP_CHECKMULTISIG
    #
    # You should verify that the script contains the pubkeys you expect
    # from the derivation path returned so that you are not blindly trusting
    # the service.
    print(address)
