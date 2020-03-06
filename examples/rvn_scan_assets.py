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

import sys
import argparse
import ravencoin
import ravencoin.core
from ravencoin.rpc import RavenProxy
from ravencoin.core import COIN
from ravencoin.core.assets import RvnAssetData
from ravencoin.core.script import OP_RVN_ASSET,CScriptOp
from ravencoin.assets import CAssetName

parser = argparse.ArgumentParser(description='Scans Ravencoin blockchain for assets using RPC')
parser.add_argument('--testnet',action="store_true",help="Use testnet (default: mainnet)")
parser.add_argument('--startblock',type=int,default=0,help="Scan starting block")
parser.add_argument('--match',type=str,default="",help="Asset name match string (default: all)")
args=parser.parse_args()

start = args.startblock
if args.testnet:
    ravencoin.SelectParams("testnet")
else:
    if args.startblock == 0:
        start = ravencoin.core.coreparams.nAssetActivationHeight
    ravencoin.SelectParams("mainnet")

r = RavenProxy() # ravencoin daemon must be running locally with rpc server enabled

try:
    end = r.getblockcount()
except Exception as e:
    print("Error: ".format(e))
    sys.exit(1)

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
                          display = True
                          if args.match != "" and not args.match in a.asset_name:
                              display = False
                          if display:
                              print(a.asset_name,a.asset_type,int(a.amount/COIN),a.ipfshash)
                          if a.asset_name != "":
                              n = CAssetName(a.asset_name) # check asset name for validity
                      except Exception as e:
                          print(e,d)

          except Exception as e:
              print(e)
