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
from ravencoin.wallet import CRavencoinAddress, P2SHRavencoinAddress, P2PKHRavencoinAddress, CRavencoinSecret
from ravencoin.core import b2x, b2lx, x

class Test_RavenAddresses(unittest.TestCase):
    def test_address_from_private_key(self):
        ravencoin.SelectParams("mainnet")
        key = CRavencoinSecret('L5gsvAVJxs9eyqeqkBDoQKjhEYxsrQABq5uG7F5rqjQMqqY4uoKo')
        self.assertEqual(b2x(key.pub),'0263af27d5f7d93de11bd19f523a633323b39aa0ee58d7d961039569caa43d3582')
        pub_addr = P2PKHRavencoinAddress.from_pubkey(key.pub)
        self.assertEqual(str(pub_addr),'RAq89qrZXWXnCsvZ8eJ6qvsufDN2qktRNB')
