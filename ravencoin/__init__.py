# Copyright (C) 2012-2018 The python-bitcoinlib developers
# Copyright (C) 2018-2020 The python-ravencoinlib developers
#
# This file is part of python-ravencoinlib.
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of python-ravencoinlib, including this file, may be copied, modified,
# propagated, or distributed except according to the terms contained in the
# LICENSE file.

from __future__ import absolute_import, division, print_function, unicode_literals

import ravencoin.core

from version import __version__


class MainParams(ravencoin.core.CoreMainParams):
    MESSAGE_START = b'\x52\x41\x56\x4e'
    DEFAULT_PORT = 8767
    RPC_PORT = 8766
    DNS_SEEDS = (('seed-raven.bitactivate.com', 'seed-raven.ravencoin.com'),
                 ('seed-raven.ravencoin.org', ''))
    BASE58_PREFIXES = {'PUBKEY_ADDR':60,
                       'SCRIPT_ADDR':122,
                       'SECRET_KEY' :128}
    BECH32_HRP = ''

class TestNetParams(ravencoin.core.CoreTestNetParams):
    MESSAGE_START = b'\x52\x56\x4e\x54'
    DEFAULT_PORT = 18770
    RPC_PORT = 18766
    DNS_SEEDS = (('seed-testnet-raven.bitactivate.com', 'seed-testnet-raven.ravencoin.com'),
                 ('seed-testnet-raven.ravencoin.org', ''))
    BASE58_PREFIXES = {'PUBKEY_ADDR':111,
                       'SCRIPT_ADDR':196,
                       'SECRET_KEY' :239}
    BECH32_HRP = ''

class RegTestParams(ravencoin.core.CoreRegTestParams):
    MESSAGE_START = b'\x43\x52\x4f\x57'
    DEFAULT_PORT = 18444
    RPC_PORT = 18443
    DNS_SEEDS = ()
    BASE58_PREFIXES = {'PUBKEY_ADDR':111,
                       'SCRIPT_ADDR':196,
                       'SECRET_KEY' :239}
    BECH32_HRP = ''

"""Master global setting for what chain params we're using.

However, don't set this directly, use SelectParams() instead so as to set the
ravencoin.core.params correctly too.
"""
#params = ravencoin.core.coreparams = MainParams()
params = MainParams()

def SelectParams(name):
    """Select the chain parameters to use

    name is one of 'mainnet', 'testnet', or 'regtest'

    Default chain is 'mainnet'
    """
    global params
    ravencoin.core._SelectCoreParams(name)
    if name == 'mainnet':
        params = ravencoin.core.coreparams = MainParams()
    elif name == 'testnet':
        params = ravencoin.core.coreparams = TestNetParams()
    elif name == 'regtest':
        params = ravencoin.core.coreparams = RegTestParams()
    else:
        raise ValueError('Unknown chain %r' % name)
