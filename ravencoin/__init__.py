# Copyright (C) 2012-2018 The python-bitcoinlib developers
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

# Note that setup.py can break if __init__.py imports any external
# dependencies, as these might not be installed when setup.py runs. In this
# case __version__ could be moved to a separate version.py and imported here.
__version__ = '0.2.0dev'

class MainParams(ravencoin.core.CoreMainParams):
    MESSAGE_START = b'\xf9\xbe\xb4\xd9'
    DEFAULT_PORT = 8333
    RPC_PORT = 8332
    DNS_SEEDS = (('ravencoin.sipa.be', 'seed.ravencoin.sipa.be'),
                 ('bluematt.me', 'dnsseed.bluematt.me'),
                 ('dashjr.org', 'dnsseed.ravencoin.dashjr.org'),
                 ('ravencoinstats.com', 'seed.ravencoinstats.com'),
                 ('xf2.org', 'bitseed.xf2.org'),
                 ('ravencoin.jonasschnelli.ch', 'seed.ravencoin.jonasschnelli.ch'))
    BASE58_PREFIXES = {'PUBKEY_ADDR':0,
                       'SCRIPT_ADDR':5,
                       'SECRET_KEY' :128}
    BECH32_HRP = 'bc'

class TestNetParams(ravencoin.core.CoreTestNetParams):
    MESSAGE_START = b'\x0b\x11\x09\x07'
    DEFAULT_PORT = 18333
    RPC_PORT = 18332
    DNS_SEEDS = (('testnetravencoin.jonasschnelli.ch', 'testnet-seed.ravencoin.jonasschnelli.ch'),
                 ('petertodd.org', 'seed.tbtc.petertodd.org'),
                 ('bluematt.me', 'testnet-seed.bluematt.me'),
                 ('ravencoin.schildbach.de', 'testnet-seed.ravencoin.schildbach.de'))
    BASE58_PREFIXES = {'PUBKEY_ADDR':111,
                       'SCRIPT_ADDR':196,
                       'SECRET_KEY' :239}
    BECH32_HRP = 'tb'

class RegTestParams(ravencoin.core.CoreRegTestParams):
    MESSAGE_START = b'\xfa\xbf\xb5\xda'
    DEFAULT_PORT = 18444
    RPC_PORT = 18443
    DNS_SEEDS = ()
    BASE58_PREFIXES = {'PUBKEY_ADDR':111,
                       'SCRIPT_ADDR':196,
                       'SECRET_KEY' :239}
    BECH32_HRP = 'bcrt'

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
