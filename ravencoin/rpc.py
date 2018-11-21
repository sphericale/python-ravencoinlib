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

from __future__ import absolute_import, division, print_function, unicode_literals
import os
import platform
import bitcoin.rpc
from ravencoin.core import lx


DEFAULT_HTTP_TIMEOUT = 30

def get_rvn_conf():
   if platform.system() == 'Darwin':
      rvn_conf_file = os.path.expanduser('~/Library/Application Support/Raven/')
   elif platform.system() == 'Windows':
      rvn_conf_file = os.path.join(os.environ['APPDATA'], 'Raven')
   else:
      rvn_conf_file = os.path.expanduser('~/.raven')
   rvn_conf_file = os.path.join(rvn_conf_file, 'raven.conf')
   return rvn_conf_file


class RavenRawProxy(bitcoin.rpc.RawProxy):
   def __init__(self,
                 service_url=None,
                 service_port=None,
                 rvn_conf_file=None,
                 timeout=DEFAULT_HTTP_TIMEOUT,
                 **kwargs):

        if service_url is None:
            if rvn_conf_file is None:
                rvn_conf_file = get_rvn_conf()

        super(RavenRawProxy, self).__init__(service_url=service_url,
                                       service_port=service_port,
                                       btc_conf_file=rvn_conf_file,
                                       timeout=timeout,
                                       **kwargs)

class RavenProxy(bitcoin.rpc.Proxy):
    def __init__(self,
                 service_url=None,
                 service_port=None,
                 rvn_conf_file=None,
                 timeout=DEFAULT_HTTP_TIMEOUT,
                 **kwargs):

        if service_url is None:
            if rvn_conf_file is None:
                rvn_conf_file = get_rvn_conf()

        super(RavenProxy, self).__init__(service_url=service_url,
                                    service_port=service_port,
                                    btc_conf_file=rvn_conf_file,
                                    timeout=timeout,
                                    **kwargs)

    """ Raven asset support """

    def issue(self, asset_name, qty=1, to_address="", change_address="", units=0, reissuable=True, has_ipfs=False, ipfs_hash=""):
        """Issue an asset with unique name.
        Unit as 0 for whole units, or 8 for satoshi-like units (0.00000001).
        Qty should be whole number.
        Reissuable is true/false for whether additional units can be issued by the original issuer."""
        r = self._call('issue', str(asset_name), float(qty), str(to_address), str(change_address), int(units), reissuable, has_ipfs, ipfs_hash)
        txid = r[0]
        return lx(txid)

    def issueunique(self, root_name, asset_tags, ipfs_hashes=None, to_address="", change_address=""):
        """Creates a unique asset from a pool of assets with a specific name.
        Example: If the asset name is SOFTLICENSE, then this could make unique assets like SOFTLICENSE#38293 and SOFTLICENSE#48382
        """
        asset_tags_str = [str(x) for x in asset_tags]
        r = self._call('issueunique', str(root_name), asset_tags_str, ipfs_hashes, str(to_address), str(change_address))
        txid = r[0]
        return lx(txid)

    def reissue(self, reissue_asset_name, qty, to_address, change_address="", reissuable=True, new_unit=-1, new_ipfs=None):
        """Issue more of a specific asset. This is only allowed by the original issuer of the asset
        and if the reissuable flag was set to true at the time of original issuance."""
        qty = float(qty)
        new_unit = int(new_unit)
        if new_ipfs is not None:
           r = self._call('reissue', str(reissue_asset_name), qty, str(to_address), str(change_address), reissuable, new_unit, new_ipfs)
        else:
           r = self._call('reissue', str(reissue_asset_name), qty, str(to_address), str(change_address), reissuable, new_unit)
        txid = r[0]
        return lx(txid)

    def transfer(self, asset_name, qty, to_address):
        """This sends assets from one asset holder to another"""
        r = self._call('transfer', str(asset_name), float(qty), str(to_address))
        txid = r[0]
        return lx(txid)

    def listassets(self, assets="*", verbose=False, count=2147483647, start=0):
        """This lists assets that have already been created"""
        r = self._call('listassets', assets, verbose, count, start)
        return r

    def listmyassets(self, asset="*", verbose=False, count=2147483647, start=0):
        """Lists your assets"""
        r = self._call('listmyassets', asset, verbose, count, start)
        return r

    def listassetbalancesbyaddress(self, address):
        """Lists asset balance by address"""
        r = self._call('listassetbalancesbyaddress', str(address))
        return r

    def listaddressesbyasset(self, asset_name):
        """Lists addresses by asset"""
        r = self._call('listaddressesbyasset', str(asset_name))
        return r

    def getassetdata(self, asset_name):
        """Lists asset data of an asset"""
        r = self._call('getassetdata', str(asset_name))
        return r
