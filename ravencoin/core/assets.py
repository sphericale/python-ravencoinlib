# Copyright (C) 2020 The python-ravencoinlib developers
#
# This file is part of python-ravencoinlib.
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of python-ravencoinlib, including this file, may be copied, modified,
# propagated, or distributed except according to the terms contained in the
# LICENSE file.

import struct

from ravencoin.base58 import encode
from ravencoin.core import x
from ravencoin.core.script import OP_RESERVED


asset_types = {

    0x74: 'transfer', #t
    0x71: 'new', #q
    0x6f: 'admin', #o
    0x72: 'reissue', #r
    0x00: 'nullassetdata'

}

null_types = {

    0: 'nullasset',
    1: 'globalrestriction',
    2: 'verifier'

}

def isnullassettype(data):

    result = False
    result_t = -1

    if len(data) > 22:
        if data[0] == 0x14:
            result = True
            result_t = 0

    elif len(data) > 5:
        if data[0] == OP_RESERVED and data[1] == OP_RESERVED:
            result = True
            result_t = 1

    elif len(data) > 2:
        if data[0] == OP_RESERVED and data[1] == OP_RESERVED:
            result = True
            result_t = 2

    return (bool(result),int(result_t))


class RvnAssetData(object):
    # representation of op_rvn_asset data structure
    def __init__(self, data=None):
        self._asset_type = None
        self._asset_name = ""
        self._amount = 0
        self._divisor = None
        self._reissuable = None
        self._ipfshash = ""
        self.data = None # raw data (bytes)
        isnull = False

        if data is not None:
            if type(data) is str:
                # pass binary or hex string to initialise object
                # data must exclude the op_rvn_asset bytecode itself
                # and the first (script length) and last (75 = OP_DROP) bytes
                data = x(data)
            self.data = data

            try:
                prefix = struct.unpack('< 3s', data[:3])[0]
                assert(prefix.decode("ascii") == "rvn")
            except Exception as e:
                self.asset_type = 0
                return # treat as nullassetdata

            self.asset_type, name_length = struct.unpack('< B B', data[3:5])

            if self.asset_type in ("new","admin","reissue","transfer"):
                # asset name
                unpack_data = data[5:5 + name_length]
                self._asset_name = struct.unpack('< {}s'.format(name_length), unpack_data)
                self._asset_name = self._asset_name[0].decode('ascii')

                if self._asset_type == 0x6f: # admin asset
                    return

                unpack_data = data[5 + name_length:5 + name_length + 8]
                self._amount = struct.unpack('< q', unpack_data)[0]

            if self.asset_type in ("new","reissue"):
                unpack_data = data[5 + name_length + 8:]
                idx = 0
                if len(unpack_data) > 0:
                    self._divisor = struct.unpack('<B',unpack_data[idx:idx+1])[0]
                    idx += 1
                if len(unpack_data) > 1:
                    self._reissuable = struct.unpack('<B',unpack_data[idx:idx+1])[0]
                    idx += 1
                if len(unpack_data) > 2 and self.asset_type == "new":
                    has_ipfs = struct.unpack('<?',unpack_data[idx:idx+1])[0]
                    idx += 1
                if len(unpack_data) > 3:
                    ipfs_bytelength = struct.unpack('<B',unpack_data[idx:idx+1])[0]
                    if ipfs_bytelength == 84:
                        idx += 1
                        ipfs_bytelength = struct.unpack('<B',unpack_data[idx:idx+1])[0]
                        idx += 1
                    ipfs_data = unpack_data[idx:]
                    self._ipfshash = struct.unpack('<{}s'.format(len(ipfs_data)), ipfs_data)[0]
                    if len(self._ipfshash) == 34:
                        self._ipfshash = encode(self._ipfshash)
                    else:
                        self._ipfshash = self._ipfshash.hex()

    @property
    def asset_type(self):
        return asset_types.get(self._asset_type, 'unknown')

    @asset_type.setter
    def asset_type(self, n):
        if n not in asset_types:
            raise ValueError("Unknown asset type {}".format(n))
        self._asset_type = n

    @property
    def asset_name(self):
        return self._asset_name

    @asset_name.setter
    def asset_name(self,s):
        if type(s) != str:
            raise ValueError("Asset name must be of type 'str'")
        self._asset_name = s

    @property
    def amount(self):
        return self._amount

    @property
    def divisor(self):
        return self._divisor

    @property
    def reissuable(self):
        return self._reissuable

    @property
    def ipfshash(self):
        return self._ipfshash
