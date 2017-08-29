""" Example of logging in a watch only user with GreenAddress """
from gacommon.utils import *
from login_authenticate import do_login
import sys


if __name__ == "__main__":

    mnemonics = sys.argv[1]

    # First, login a full user to create the watch only account
    conn, wallet, login_data = do_login(mnemonics)

    # Find out if we have a watch only account already set up
    sync_data = conn.call('addressbook.get_sync_status')
    have_watch_only = sync_data['username'] is not None

    # For example purposes, create a user/password based on the mnemonics.
    watch_only_username = h(sha256(bytearray(mnemonics, 'ascii')))[:15]
    watch_only_password = h(sha256(bytearray(mnemonics + 'dummy', 'ascii')))[:15]

    # Create the watch only user if we don't already have one
    if not have_watch_only:
        ret = conn.call('addressbook.sync_custom',
                        watch_only_username, watch_only_password)
        assert ret

    # Login the watch only user
    watch_only_conn = GAConnection(GAConnection.REGTEST_URI)
    testnet = True

    token = {'username': watch_only_username,
             'password': watch_only_password}
    login_data = watch_only_conn.call('login.watch_only_v2', 'custom', token,
                                      GAConnection.USER_AGENT)

    # The watch only user can now be used to fetch addresses etc
    print(login_data)
