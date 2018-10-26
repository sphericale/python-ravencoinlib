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

from __future__ import absolute_import, division, print_function, unicode_literals
from bitcoin.wallet import *

class CRavencoinAddress(CBitcoinAddress):
    pass

class P2SHRavencoinAddress(P2SHBitcoinAddress):
    pass

class P2PKHRavencoinAddress(P2PKHBitcoinAddress):
    pass

class CRavencoinSecret(CBitcoinSecret, CKey):
    def __init__(self, s):
        super(CRavencoinSecret, self).__init__(s)


