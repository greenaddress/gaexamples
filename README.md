GreenAddress API examples

This repository is a collection of python example programs to illustrate
how to use the GreenAddress API.

All examples run against the GreenAddress regtest service by default. This
service is provided for experimentation and development only. We reserve the
right to restart or delete data from regtest as needed to maintain its utility
as a testbed for users developing against the API.

Please do not use real mnemonics or attempt to store secure, identifying or
important data on the regtest service.

For more information on the GreenAddress service and our API, please read the
[GreenAddress FAQ](https://greenaddress.it/en/faq) and the
[GreenAddress API Documentation](https://api.greenaddress.it/).

We intend to add more examples and improve the documentation in the future.
For more examples of real world API usage including key derivation, etc.
please see the source code of:

* Python: [garecovery tool](https://github.com/greenaddress/garecovery).
* Java: [GreenBits Wallet](https://github.com/greenaddress/GreenBits).
* JavaScript: [GreenAddress WebFiles](https://github.com/greenaddress/GreenAddressWebFiles).

# Dependencies for Ubuntu & Debian
Remove all '{,3}' if you want to use just python2
```
$ sudo apt-get update -qq
$ sudo apt-get install python{,3}-pip python{,3}-dev build-essential python{,3}-virtualenv -yqq
```

# Install
```
$ virtualenv [-p python3] venv
$ source venv/bin/activate
$ pip install --require-hashes -r tools/requirements.txt
```

# Run examples

First run `create_mnemonic.py` to create mnemonics for testing.
```
$ python create_mnemonics.py
```

Register the user with the service.
```
$ python login_register.py "words printed by create mnemonics ..."
```

The examples are named after the module and function they demonstrate. You
should run them by passing the mnemonics as the first argument.
```
$ python module_function_name.py "your mnemonic words here ..."
```

# Troubleshooting

If you find any bugs, or have suggestions or patches, please raise them on
the [gaexamples github project](https://github.com/greenaddress/gaexamples).
