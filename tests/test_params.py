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

import unittest

import ravencoin
import ravencoin.core
from ravencoin.core import b2lx

COIN = 100000000 # from amount.h

class Test_RavenParams(unittest.TestCase):
    def test_mainnet_params(self):
        ravencoin.SelectParams("mainnet")
        params = ravencoin.GetParams()
        self.assertEqual(params.MESSAGE_START, b'\x52\x41\x56\x4e')
        self.assertEqual(params.DEFAULT_PORT, 8767)
        self.assertEqual(params.RPC_PORT, 8766)
        self.assertEqual(params.BASE58_PREFIXES['PUBKEY_ADDR'],60)
        self.assertEqual(params.BASE58_PREFIXES['SCRIPT_ADDR'],122)
        self.assertEqual(params.BASE58_PREFIXES['SECRET_KEY'],128)

    def test_testnet_params(self):
        ravencoin.SelectParams("testnet")
        params = ravencoin.GetParams()
        self.assertEqual(params.MESSAGE_START, b'\x52\x56\x4e\x54')
        self.assertEqual(params.DEFAULT_PORT, 18770)
        self.assertEqual(params.RPC_PORT, 18766)
        self.assertEqual(params.BASE58_PREFIXES['PUBKEY_ADDR'],111)
        self.assertEqual(params.BASE58_PREFIXES['SCRIPT_ADDR'],196)
        self.assertEqual(params.BASE58_PREFIXES['SECRET_KEY'],239)

    def test_regtest_params(self):
        ravencoin.SelectParams("regtest")
        params = ravencoin.GetParams()
        self.assertEqual(params.MESSAGE_START, b'\x43\x52\x4f\x57')
        self.assertEqual(params.DEFAULT_PORT, 18444)
        self.assertEqual(params.RPC_PORT, 18443)
        self.assertEqual(params.BASE58_PREFIXES['PUBKEY_ADDR'],111)
        self.assertEqual(params.BASE58_PREFIXES['SCRIPT_ADDR'],196)
        self.assertEqual(params.BASE58_PREFIXES['SECRET_KEY'],239)


    def test_mainnet_coreparams(self):
        ravencoin.SelectParams("mainnet")
        params = ravencoin.core.GetParams()
        self.assertEqual(params.MAX_MONEY,21000000000*COIN)
        self.assertEqual(params.SUBSIDY_HALVING_INTERVAL,2100000)
        self.assertEqual(params.PROOF_OF_WORK_LIMIT,0x00000fffffffffffffffffffffffffffffffffffffffffffffffffffffffffff)

    def test_testnet_coreparams(self):
        ravencoin.SelectParams("testnet")
        params = ravencoin.core.GetParams()
        self.assertEqual(params.MAX_MONEY,21000000000*COIN)
        self.assertEqual(params.SUBSIDY_HALVING_INTERVAL,2100000)
        self.assertEqual(params.PROOF_OF_WORK_LIMIT,0x00000fffffffffffffffffffffffffffffffffffffffffffffffffffffffffff)

    def test_regtest_coreparams(self):
        ravencoin.SelectParams("regtest")
        params = ravencoin.core.GetParams()
        self.assertEqual(params.MAX_MONEY,21000000000*COIN)
        self.assertEqual(params.SUBSIDY_HALVING_INTERVAL,150)
        self.assertEqual(params.PROOF_OF_WORK_LIMIT,0x7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff)


