# Copyright (C) 2018 The python-ravencoinlib developers
#
# This file is part of python-ravencoinlib.
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of python-ravencoinlib, including this file, may be copied, modified,
# propagated, or distributed except according to the terms contained in the
# LICENSE file.

import bitcoin
import bitcoin.core
import ravencoin.core

class MainParams(bitcoin.core.CoreMainParams):
    MESSAGE_START = b'\x52\x41\x56\x4e'
    DEFAULT_PORT = 8767
    RPC_PORT = 8766
    DNS_SEEDS = (('seed-raven.bitactivate.com', 'seed-raven.ravencoin.com'),
                 ('seed-raven.ravencoin.org', ''))
    BASE58_PREFIXES = {'PUBKEY_ADDR':60,
                       'SCRIPT_ADDR':122,
                       'SECRET_KEY' :128}

class TestNetParams(bitcoin.core.CoreTestNetParams):
    MESSAGE_START = b'\x52\x56\x4e\x54'
    DEFAULT_PORT = 18770
    RPC_PORT = 18766
    DNS_SEEDS = (('seed-testnet-raven.bitactivate.com', 'seed-testnet-raven.ravencoin.com'),
                 ('seed-testnet-raven.ravencoin.org', ''))
    BASE58_PREFIXES = {'PUBKEY_ADDR':111,
                       'SCRIPT_ADDR':196,
                       'SECRET_KEY' :239}

class RegTestParams(bitcoin.core.CoreRegTestParams):
    MESSAGE_START = b'\x43\x52\x4f\x57'
    DEFAULT_PORT = 18444
    RPC_PORT = 18443
    DNS_SEEDS = ()
    BASE58_PREFIXES = {'PUBKEY_ADDR':111,
                       'SCRIPT_ADDR':196,
                       'SECRET_KEY' :239}


# monkey patch the bitcoin params
bitcoin.MainParams = MainParams
bitcoin.TestNetParams = TestNetParams
bitcoin.RegTestParams = RegTestParams

bitcoin.SelectParams("mainnet")

def SelectParams(name):
    """Select the chain parameters to use

    name is one of 'mainnet', 'testnet', or 'regtest'

    Default chain is 'mainnet'
    """
    bitcoin.SelectParams(name)

def GetParams():
    return bitcoin.params
