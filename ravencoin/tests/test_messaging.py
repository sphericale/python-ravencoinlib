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

import unittest

import ravencoin
from ravencoin.assets import CMainAsset, CSubAsset, CUniqueAsset, InvalidAssetName, InvalidAssetType
from ravencoin.messaging import CMessageChannel, InvalidChannelName

ravencoin.SelectParams("mainnet")

class Test_ChannelNames(unittest.TestCase):
    def test_invalidnames(self):

        main_asset = CMainAsset("MAIN")
        sub_asset = CSubAsset("SUB",parent=main_asset)

        # too long
        with self.assertRaises(InvalidChannelName):
            CMessageChannel("CHANNELXXXXXXXX",parent=main_asset)

        # valid channel name, but too long total length
        with self.assertRaises(InvalidChannelName):
            CMessageChannel("CHANNEL",parent=CMainAsset("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"))

        main_asset = CMainAsset("1234567890")
        sub_asset = CSubAsset("1234567890",parent=main_asset)
        with self.assertRaises(InvalidChannelName):
            CMessageChannel("AAAAAAAAAAA",parent=sub_asset)



    def test_validnames(self):
        main_asset = CMainAsset("MAIN1")
        sub_asset = CSubAsset("SUB1",parent=main_asset)

        msg_channel = CMessageChannel("CHANNEL",parent=main_asset)
        self.assertTrue(msg_channel.name == "CHANNEL")

        msg_channel = CMessageChannel("CHAN1",parent=main_asset)
        self.assertTrue(str(msg_channel) == "MAIN1~CHAN1")

        msg_channel = CMessageChannel("CHAN2",parent=sub_asset)
        self.assertTrue(str(msg_channel) == "MAIN1/SUB1~CHAN2")

