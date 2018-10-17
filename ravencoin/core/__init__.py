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

import sys
import bitcoin.core
from bitcoin.core import *
from bitcoin.core.script import OP_RETURN

if sys.version > '3':
    _bytes = bytes
else:
    _bytes = lambda x: bytes(bytearray(x))

# Core definitions
COIN = 100000000
MAX_BLOCK_SIZE = 2000000 # after assets deployed
MAX_BLOCK_WEIGHT = 8000000
MAX_BLOCK_SIGOPS = MAX_BLOCK_SIZE/50 # 25?
WITNESS_COINBASE_SCRIPTPUBKEY_MAGIC = _bytes([OP_RETURN, 0x24, 0xaa, 0x21, 0xa9, 0xed])

class CoreMainParams(bitcoin.core.CoreChainParams):
    MAX_MONEY = 21000000000 * COIN
    NAME = 'mainnet'
    GENESIS_BLOCK = CBlock.deserialize(x('04000000000000000000000000000000000000000000000000000000000000000000000016355fae8b6a26f2fa708d39997654c44b501f308d802325359a7367a800ff28c60e4d5affff001ee0d47d010101000000010000000000000000000000000000000000000000000000000000000000000000ffffffff570004ffff001d01044c4d5468652054696d65732030332f4a616e2f3230313820426974636f696e206973206e616d65206f66207468652067616d6520666f72206e65772067656e65726174696f6e206f66206669726d73ffffffff010088526a74000000434104678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac00000000'))
    SUBSIDY_HALVING_INTERVAL = 2100000
    PROOF_OF_WORK_LIMIT = 2**256-1 >> 20

    # Burn Amounts
    nIssueAssetBurnAmount = 500 * COIN
    nReissueAssetBurnAmount = 100 * COIN
    nIssueSubAssetBurnAmount = 100 * COIN
    nIssueUniqueAssetBurnAmount = 5 * COIN

    # Burn Addresses
    strIssueAssetBurnAddress = "RXissueAssetXXXXXXXXXXXXXXXXXhhZGt"
    strReissueAssetBurnAddress = "RXReissueAssetXXXXXXXXXXXXXXVEFAWu"
    strIssueSubAssetBurnAddress = "RXissueSubAssetXXXXXXXXXXXXXWcwhwL"
    strIssueUniqueAssetBurnAddress = "RXissueUniqueAssetXXXXXXXXXXWEAe58"

    # Global Burn Address
    strGlobalBurnAddress = "RXBurnXXXXXXXXXXXXXXXXXXXXXXWUo9FV"


class CoreTestNetParams(bitcoin.core.CoreMainParams):
    MAX_MONEY = 21000000000 * COIN
    NAME = 'testnet'
    GENESIS_BLOCK = CBlock.deserialize(x('02000000000000000000000000000000000000000000000000000000000000000000000016355fae8b6a26f2fa708d39997654c44b501f308d802325359a7367a800ff2820e0a35bffff001e8847ee000101000000010000000000000000000000000000000000000000000000000000000000000000ffffffff570004ffff001d01044c4d5468652054696d65732030332f4a616e2f3230313820426974636f696e206973206e616d65206f66207468652067616d6520666f72206e65772067656e65726174696f6e206f66206669726d73ffffffff010088526a74000000434104678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac00000000'))
    SUBSIDY_HALVING_INTERVAL = 2100000
    PROOF_OF_WORK_LIMIT = 2**256-1 >> 20

    # Burn Amounts
    nIssueAssetBurnAmount = 500 * COIN;
    nReissueAssetBurnAmount = 100 * COIN;
    nIssueSubAssetBurnAmount = 100 * COIN;
    nIssueUniqueAssetBurnAmount = 5 * COIN;

    # Burn Addresses
    strIssueAssetBurnAddress = "n1issueAssetXXXXXXXXXXXXXXXXWdnemQ"
    strReissueAssetBurnAddress = "n1ReissueAssetXXXXXXXXXXXXXXWG9NLd"
    strIssueSubAssetBurnAddress = "n1issueSubAssetXXXXXXXXXXXXXbNiH6v"
    strIssueUniqueAssetBurnAddress = "n1issueUniqueAssetXXXXXXXXXXS4695i"

    # Global Burn Address
    strGlobalBurnAddress = "n1BurnXXXXXXXXXXXXXXXXXXXXXXU1qejP"

class CoreRegTestParams(bitcoin.core.CoreTestNetParams):
    MAX_MONEY = 21000000000 * COIN
    NAME = 'regtest'
    GENESIS_BLOCK = CBlock.deserialize(x('04000000000000000000000000000000000000000000000000000000000000000000000016355fae8b6a26f2fa708d39997654c44b501f308d802325359a7367a800ff28a621d95affff7f20010000000101000000010000000000000000000000000000000000000000000000000000000000000000ffffffff570004ffff001d01044c4d5468652054696d65732030332f4a616e2f3230313820426974636f696e206973206e616d65206f66207468652067616d6520666f72206e65772067656e65726174696f6e206f66206669726d73ffffffff010088526a74000000434104678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac00000000'))
    SUBSIDY_HALVING_INTERVAL = 150
    PROOF_OF_WORK_LIMIT = 2**256-1 >> 1

    # Burn Amounts
    nIssueAssetBurnAmount = 500 * COIN;
    nReissueAssetBurnAmount = 100 * COIN;
    nIssueSubAssetBurnAmount = 100 * COIN;
    nIssueUniqueAssetBurnAmount = 5 * COIN;

    # Burn Addresses
    strIssueAssetBurnAddress = "n1issueAssetXXXXXXXXXXXXXXXXWdnemQ"
    strReissueAssetBurnAddress = "n1ReissueAssetXXXXXXXXXXXXXXWG9NLd"
    strIssueSubAssetBurnAddress = "n1issueSubAssetXXXXXXXXXXXXXbNiH6v"
    strIssueUniqueAssetBurnAddress = "n1issueUniqueAssetXXXXXXXXXXS4695i"

    # Global Burn Address
    strGlobalBurnAddress = "n1BurnXXXXXXXXXXXXXXXXXXXXXXU1qejP"


# monkey patching
bitcoin.core.COIN = COIN
bitcoin.core.MAX_BLOCK_SIZE = MAX_BLOCK_SIZE
bitcoin.core.MAX_BLOCK_WEIGHT = MAX_BLOCK_WEIGHT
bitcoin.core.MAX_BLOCK_SIGOPS = MAX_BLOCK_SIGOPS
bitcoin.core.WITNESS_COINBASE_SCRIPTPUBKEY_MAGIC = WITNESS_COINBASE_SCRIPTPUBKEY_MAGIC

bitcoin.core.CoreMainParams = CoreMainParams
bitcoin.core.CoreTestNetParams = CoreTestNetParams
bitcoin.core.CoreRegTestParams = CoreRegTestParams


def GetParams():
    return bitcoin.core.coreparams
