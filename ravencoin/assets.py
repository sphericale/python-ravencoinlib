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

"""Ravencoin assets"""

import re

sha_256_hash = re.compile("^[A-Fa-f0-9]{64}$") # regex matching a sha256 hash

# Asset metadata representation
# https://github.com/RavenProject/Ravencoin/blob/master/assets/asset_metadata_spec.md

class Asset_Metadata(object):
    def __init__(self, contract_url="", contract_hash="", contract_signature="",
                contract_address="", symbol="", name="", issuer="", description="", description_mime="",
                type="", website_url="", icon="", image_url="", contact_name="", contact_email="",
                contact_address="", contact_phone="", forsale=None, forsale_price="", forsale_price_currency="", restricted="", validate=True):

        self._validate = validate # if True, attempt to validate fields

        self.contract_url = contract_url
        self.contract_hash = contract_hash
        self.contract_signature = contract_signature
        self.contract_address = contract_address
        self.symbol = symbol
        self.name = name
        self.issuer = issuer
        self.description = description
        self.description_mime = description_mime
        self.type = type
        self.website_url = website_url
        self.icon = icon
        self.image_url = image_url
        self.contact_name = contact_name
        self.contact_email = contact_email
        self.contact_address = contact_address
        self.contact_phone = contact_phone
        self.forsale = forsale
        # currency and price can be given separately
        # otherwise assume forsale_price is already formatted e.g. "1000 USD" as spec
        if (forsale_price != "") and (forsale_price_currency != ""):
            self.forsale_price = forsale_price+" "+forsale_price_currency
        else:
            self.forsale_price = forsale_price
        self.restricted = restricted

    def __str__(self):
        """ Returns json serializable string """
        import json
        return json.dumps(dict((key, value) for key, value in iter([
              ("contract_url",self.contract_url),
              ("contract_hash",self.contract_hash),
              ("contract_signature",self.contract_signature),
              ("contract_address",self.contract_address),
              ("symbol",self.symbol),
              ("name",self.name),
              ("issuer",self.issuer),
              ("description",self.description),
              ("description_mime",self.description_mime),
              ("type",self.type),
              ("website_url",self.website_url),
              ("icon",self.icon),
              ("image_url",self.image_url),
              ("contact_name",self.contact_name),
              ("contact_email",self.contact_email),
              ("contact_address",self.contact_address),
              ("contact_phone",self.contact_phone),
              ("forsale",self.forsale),
              ("forsale_price",self.forsale_price),
              ("restricted",self.restricted)
              ]) if value is not None and value != ""))

    @property
    def contract_hash(self):
        return self._contract_hash

    @contract_hash.setter
    def contract_hash(self,hashstr):
        if not self._validate or hashstr == "":
            self._contract_hash = hashstr
        else:
            if sha_256_hash.match(hashstr):
               self._contract_hash = hashstr
            else:
               raise ValueError("contract_hash must be a sha256 hash in ascii hex")

