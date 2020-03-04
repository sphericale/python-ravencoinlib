#!/usr/bin/env python3
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

import ravencoin
import ravencoin.core
from ravencoin.rpc import RavenProxy
from ravencoin.core.assets import RvnAssetData
from ravencoin.core.script import OP_RVN_ASSET,CScriptOp

ravencoin.SelectParams("mainnet")

r = RavenProxy() # ravencoin daemon must be running locally with rpc server enabled

start = ravencoin.core.coreparams.nAssetActivationHeight
end = r.getblockcount()

for c in range(start,end):
   blockhash = r.getblockhash(c)
   block = r.getblock(blockhash)
   for tx in block.vtx:
      for v in tx.vout:
          try:
               get_data = False
               data = []
               for x in v.scriptPubKey:
                  if x == OP_RVN_ASSET:
                      get_data = True    # found OP_RVN_ASSET, 1 or more data pushes follow
                      continue
                  if get_data:
                      if type(x) is not CScriptOp:
                          data.append(x) # collect up the data
                      else:
                          get_data = False
               if len(data) > 0:
                   for d in data:
                      try:
                          a = RvnAssetData(d) # parse rvn asset data as python object
                          print(a.asset_name,a.asset_type,int(a.amount/10e7))
                      except Exception as e:
                          print(e,d)

          except Exception as e:
              print(e)
