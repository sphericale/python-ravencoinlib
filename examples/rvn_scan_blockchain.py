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

import sys,os
import argparse
import re
from ravencoin.blockchain import Blockchain
from ravencoin.core import b2x,b2lx, COIN
from ravencoin.wallet import CRavencoinAddress,CRavencoinAddressError
from ravencoin.core.script import OP_RETURN

parser = argparse.ArgumentParser(description='Scans Ravencoin block database files (blk*.dat) for text in OP_RETURNs')
parser.add_argument('-D', '--dir',default="~/.raven/blocks/",type=str,help="Directory containing Ravencoin block database")
parser.add_argument('-S', '--startblock',default=0,type=int,help="Scan starting block (default: 0)")
parser.add_argument('-E', '--endblock',default=0,type=int,help="Scan ending block (default: all)")
parser.add_argument('--cachefile',default="",type=str,help="Block database index cache filename (default: no caching)")
parser.add_argument('--extendedcharsets',action="store_true",help="Try more character sets (default: ascii)")
args=parser.parse_args()

blockchain_path = os.path.expanduser(args.dir)
index_path = blockchain_path + "/index"
print("Blockhain database path {}".format(blockchain_path))
print("Index path {}".format(index_path))
if args.cachefile != "":
    print("Using index cache file {}".format(args.cachefile))

endblock = None
if args.endblock > 0:
    endblock = args.endblock

if args.extendedcharsets:
    charsets = ['ascii','utf_8','latin_1','cp1252','big5']
else:
    charsets = ['ascii']

print("Using charsets: {}".format(str(charsets).strip('[]')))

print("Scanning blocks {}-{}".format(args.startblock,endblock if endblock is not None else "all"))
print("Loading index... (this might take a while)")

ignore_re_str = [
"^\d{3}-\d{3}-\d{3}-\d{3}\:",
"^SAFE"
]

ignore_regex = []
for x in ignore_re_str:
    ignore_regex.append(re.compile(x))


blockchain = Blockchain(blockchain_path)
c = args.startblock
for block in blockchain.get_ordered_blocks(index_path, start=args.startblock, end=endblock, cache=args.cachefile):
    if c % 10000 == 0:
        print("Block {}".format(c),flush=True)
    c += 1
    for tx in block.vtx:
       hash = b2lx(tx.GetTxid())
       for vin in tx.vin:
           pass
       for vout in tx.vout:
           spk = vout.scriptPubKey
           if spk.is_witness_scriptpubkey():
               continue
           if spk[2:6] == b'\xaa\x21\xa9\xed': # segwit
               continue
           try:
               ops = [x for x in spk]
           except Exception:
               ops = []
           if OP_RETURN in ops:
               idx = ops.index(OP_RETURN)
               data = ops[idx+1]
               for charset in charsets:
                   try:
                       decoded = ""
                       decoded = data.decode(charset)
                       if decoded != "":
                           for regex in ignore_regex:
                               if regex.match(decoded) is not None:
                                   break
                           else:
                               print("{},{}".format(hash,decoded))
                               break
                   except Exception as e:
                       pass
