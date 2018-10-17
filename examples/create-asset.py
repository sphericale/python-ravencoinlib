#!/usr/bin/env python3

# simple example of asset creation using ravencoinlib

import ravencoin
from ravencoin.rpc import RavenProxy
from ravencoin.core import b2lx

ravencoin.SelectParams("testnet")


rvn = RavenProxy() # will use local daemon, must be running with the rpc server enabled

asset_name = "BTC" # your asset name
qty = 21000000 # quantity to issue

# wallet must be unlocked or this will fail

r = rvn.issue(asset_name, qty)

print("Created asset {}, txid: {}".format(asset_name,b2lx(r)))

