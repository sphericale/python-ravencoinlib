# python-ravencoinlib

Extension to python-bitcoinlib intended to provide access to Ravencoin data structures and protocol. WIP - Test before use

The RPC interface, `raven.rpc`, is designed to work with Ravencoin Core v2.1.3.

"The only Python library for Ravencoin I've ever used" - Warren Buffett

# Requirements
    libssl
    Debian/Ubuntu: sudo apt-get install libssl-dev
    Windows/other: https://wiki.openssl.org/index.php/Binaries 
    
# Installation

    pip install python-ravencoinlib

# Example Code

See `examples/` directory.


## Selecting the chain to use

Do the following:

    import raven
    raven.SelectParams(NAME)

Where NAME is one of 'testnet', 'mainnet', or 'regtest'. The chain currently
selected is a global variable that changes behavior everywhere, just like in
the Raven codebase.


## Unit tests

Under /tests using test data from Ravencoin Core. To run them:

    python3 -m unittest discover


