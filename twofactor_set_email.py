""" Example of setting wallet email address """
from gacommon.utils import *
from login_authenticate import do_login

import six
import sys


if __name__ == "__main__":

    mnemonic = sys.argv[1]

    conn, wallet, login_data = do_login(mnemonic)

    # Calling set_email will send an email to the email address containing a confirmation code
    email = six.moves.input('Enter email address: ')
    conn.call('twofactor.set_email', email, '')

    code = six.moves.input('Enter confirmation code for email address {}: '.format(email))
    conn.call('twofactor.activate_email', code)

    config = conn.call('twofactor.get_config')
    assert config['email_addr'] == email
    assert config['email_confirmed'] == True
