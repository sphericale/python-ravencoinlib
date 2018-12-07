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
from ravencoin.assets import CMainAsset, CSubAsset, CUniqueAsset, InvalidAssetName, InvalidAssetType

ravencoin.SelectParams("mainnet")

class Test_AssetNames(unittest.TestCase):
    def test_invalidnames(self):
    
        main_asset = CMainAsset("VALID")
    
        # too long
        with self.assertRaises(InvalidAssetName):
            CMainAsset("ASSETNAMETOOLONGXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            
        # valid subasset name, but too long total length (main + sub)
        with self.assertRaises(InvalidAssetName):
            CSubAsset("ASSETNAMETOOLONGXXXXXXXXX",parent=main_asset)
        
        # lowercase not allowed in main and sub       
        with self.assertRaises(InvalidAssetName):
            CMainAsset("assetname")
            
        with self.assertRaises(InvalidAssetName):
            CSubAsset("assetname",parent=main_asset)
            
        # bad characters
        with self.assertRaises(InvalidAssetName):
            CMainAsset("INVALID^()")
        with self.assertRaises(InvalidAssetName):
            CSubAsset("INVALID^()",parent=main_asset)
        with self.assertRaises(InvalidAssetName):
            CUniqueAsset("INVALID^",parent=main_asset)

        with self.assertRaises(InvalidAssetName):
            CMainAsset("RAVEN")

            
    def test_validnames(self):
        main_asset = CMainAsset("VALID.NAME")
        self.assertTrue(main_asset.name == "VALID.NAME")
        
        sub_asset = CSubAsset("1",parent=main_asset)
        self.assertTrue(sub_asset.name == "1")
        
        asset = CUniqueAsset("@1000000$()",parent=sub_asset)
        self.assertTrue(asset.name == "@1000000$()")
        
        asset = CUniqueAsset("[]{}AA:?&$",parent=sub_asset)
        self.assertTrue(asset.name == "[]{}AA:?&$")
        
        asset = CUniqueAsset("assetname",parent=sub_asset)
        self.assertTrue(asset.name == "assetname")
        
    def test_fullstr(self):
        main_asset = CMainAsset("VALID.NAME")
        sub_asset = CSubAsset("1",parent=main_asset)
        self.assertTrue(str(sub_asset) == "VALID.NAME/1")

        uniq_asset = CUniqueAsset("TEST",parent=sub_asset)
        self.assertTrue(uniq_asset.full_name == "VALID.NAME/1#TEST")
        self.assertTrue(str(uniq_asset) == "TEST")

        
    def test_ownership_tokens(self):
        ownership_token = CMainAsset("VALID.NAME",ownership=True)
        self.assertTrue(ownership_token.name == "VALID.NAME!")
        
        with self.assertRaises(InvalidAssetType):
            CSubAsset("VALID",parent=ownership_token)
            
        with self.assertRaises(InvalidAssetType):
            CUniqueAsset("VALID",parent=ownership_token)
        