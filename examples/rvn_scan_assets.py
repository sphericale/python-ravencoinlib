#!/usr/bin/env python3

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
