#!/usr/bin/env python3
# Based on burn-btc By James C. Stroud

import sys
import binascii
import argparse

from hashlib import sha256

from ravencoin.base58 import encode as b58encode
from ravencoin.base58 import decode as b58decode
from ravencoin.wallet import CRavencoinAddress, CRavencoinAddressError

ABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
template_default = "RVNBurnTest"

parser = argparse.ArgumentParser(description='Generate a Ravencoin burn address.')
parser.add_argument("template",help="Template for burn address. Max 28 letters & numbers (no zeros). Longer strings will be truncated",nargs='?',default=template_default)

class BurnError(Exception):
  pass

class AlphabetError(BurnError):
  pass

def hh256(s):
  s = sha256(s).digest()
  return binascii.hexlify(sha256(s).digest())

def b58ec(s):
  unencoded = bytearray.fromhex(s.decode())
  encoded = b58encode(unencoded)
  return encoded

def b58dc(encoded, trim=0):
  unencoded = b58decode(encoded)[:-trim]
  return unencoded

def burn(s):
  decoded = b58dc(s, trim=4)
  decoded_hex = binascii.hexlify(decoded)
  check = hh256(decoded)[:8]
  coded = decoded_hex + check
  return b58ec(coded)

if __name__ == "__main__":
  args = parser.parse_args()
  template = args.template
  if template[0] != "R":
     raise AlphabetError("Template must begin with the letter R")
  for c in template:
    if c not in ABET:
      raise AlphabetError("Character {} is not valid base58.".format(c))
    tlen = len(template)
    if tlen < 34:
      template = template + ((34 - tlen) * "X")
    else:
      template = template[:34]
  try:
     burn_address = CRavencoinAddress(burn(template))
     print(burn_address)
  except CRavencoinAddressError:
     print("'{}' is not a valid template (Must begin with the letter R followed by a capital letter e.g. 'RV')".format(args.template))

