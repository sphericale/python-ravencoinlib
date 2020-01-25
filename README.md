# python-ravencoinlib

Ravencoin fork of python-bitcoinlib intended to provide access to Ravencoin data 
structures and protocol. WIP - Test before use

The RPC interface, ravencoin.rpc, is designed to work with Ravencoin Core v3.3.0+.

"The only Python library for Ravencoin I've ever used" - Warren Buffett

## Requirements

    libssl
    Debian/Ubuntu: sudo apt-get install libssl-dev
    Windows/other: https://wiki.openssl.org/index.php/Binaries 

## Structure

Everything consensus critical is found in the modules under ravencoin.core. This
rule is followed pretty strictly, for instance chain parameters are split into
consensus critical and non-consensus-critical.

    ravencoin.core            - Basic core definitions, datastructures, and
                              (context-independent) validation
    ravencoin.core.key        - ECC pubkeys
    ravencoin.core.script     - Scripts and opcodes
    ravencoin.core.scripteval - Script evaluation/verification
    ravencoin.core.serialize  - Serialization

In the future the ravencoin.core may use the Satoshi sourcecode directly as a
library. Non-consensus critical modules include the following:

    ravencoin          - Chain selection
    ravencoin.base58   - Base58 encoding
    ravencoin.bloom    - Bloom filters (incomplete)
    ravencoin.net      - Network communication (in flux)
    ravencoin.messages - Network messages (in flux)
    ravencoin.rpc      - Ravencoin Core RPC interface support
    ravencoin.wallet   - Wallet-related code, currently Ravencoin address and
                       private key support

Effort has been made to follow the Satoshi source relatively closely, for
instance Python code and classes that duplicate the functionality of
corresponding Satoshi C++ code uses the same naming conventions: CTransaction,
CBlockHeader, nValue etc. Otherwise Python naming conventions are followed.


## Mutable vs. Immutable objects

Like the Ravencoin Core codebase CTransaction is immutable and
CMutableTransaction is mutable; unlike the Ravencoin Core codebase this
distinction also applies to COutPoint, CTxIn, CTxOut, and CBlock.


## Endianness Gotchas

Rather confusingly Ravencoin Core shows transaction and block hashes as
little-endian hex rather than the big-endian the rest of the world uses for
SHA256. python-ravencoinlib provides the convenience functions x() and lx() in
ravencoin.core to convert from big-endian and little-endian hex to raw bytes to
accomodate this. In addition see b2x() and b2lx() for conversion from bytes to
big/little-endian hex.


## Module import style

While not always good style, it's often convenient for quick scripts if
`import *` can be used. To support that all the modules have `__all__` defined
appropriately.


# Example Code

See `examples/` directory. For instance this example creates a transaction
spending a pay-to-script-hash transaction output:

    $ PYTHONPATH=. examples/spend-pay-to-script-hash-txout.py
    <hex-encoded transaction>


## Selecting the chain to use

Do the following:

    import ravencoin
    ravencoin.SelectParams(NAME)

Where NAME is one of 'testnet', 'mainnet', or 'regtest'. The chain currently
selected is a global variable that changes behavior everywhere, just like in
the Satoshi codebase.


## Unit tests

Under ravencoin/tests using test data from Ravencoin Core. To run them:

    python3 -m unittest discover

Alternately, if Tox (see https://tox.readthedocs.org/) is available on your
system, you can run unit tests for multiple Python versions:

    ./runtests.sh

HTML coverage reports can then be found in the htmlcov/ subdirectory.

## Documentation

Sphinx documentation is in the "doc" subdirectory. Run "make help" from there
to see how to build. You will need the Python "sphinx" package installed.

Currently this is just API documentation generated from the code and
docstrings. Higher level written docs would be useful, perhaps starting with
much of this README. Pages are written in reStructuredText and linked from
index.rst.
