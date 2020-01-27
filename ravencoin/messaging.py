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

"""Ravencoin messaging"""

from __future__ import absolute_import, division, print_function, unicode_literals
from ravencoin.assets import CMainAsset,CSubAsset,MAX_NAME_LENGTH

MAX_CHANNEL_NAME_LENGTH = 12

class InvalidChannelName(Exception):
    pass

class CMessageChannel(object):
    def __init__(self,name,parent=None):
        self.parent = parent
        self.name = name

    @property
    def full_name(self):
        return self.parent.full_name + '~' + self.name

    def __str__(self):
        return self.full_name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self,namestr):
    # check for invalid channel name
        if len(namestr) > MAX_CHANNEL_NAME_LENGTH:
            raise InvalidChannelName("Channel name {} is too long (max {} characters)".format(namestr,MAX_CHANNEL_NAME_LENGTH))
        self._name = namestr
    # check full name "ASSET~CHANNEL" as well
        if len(str(self)) > MAX_NAME_LENGTH:
            raise InvalidChannelName("Channel name {} is too long (max {} characters)".format(str(self),MAX_NAME_LENGTH))

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self,parent):
        if parent is None or (not isinstance(parent, CMainAsset) and not isinstance(parent, CSubAsset)):
            raise InvalidChannelName("Messaging channel requires parent of type CMainAsset or CSubAsset")
        self._parent = parent


