# Copyright (C) 2013-2015 The python-bitcoinlib developers
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

import hashlib
import unittest

from ravencoin.core import b2x, x
from ravencoin.core.script import CScript, IsLowDERSignature
from ravencoin.core.key import CPubKey, is_libsec256k1_available, use_libsecp256k1_for_signing
from ravencoin.wallet import *

class Test_CRavencoinAddress(unittest.TestCase):
    def test_create_from_string(self):
        """Create CRavencoinAddress's from strings"""

        def T(str_addr, expected_bytes, expected_version, expected_class):
            addr = CRavencoinAddress(str_addr)
            self.assertEqual(addr.to_bytes(), expected_bytes)
            self.assertEqual(addr.__class__, expected_class)
            if isinstance(addr, CBase58RavencoinAddress):
                self.assertEqual(addr.nVersion, expected_version)
            elif isinstance(addr, CBech32RavencoinAddress):
                self.assertEqual(addr.witver, expected_version)

        T('RXCTT97MGsrguKrtcF7ewXBewdGrx8o1Hg',
          x('f06d8520dbc8719c46e9b771a1233fcd74e69b2c'), 60,
          P2PKHRavencoinAddress)

        T('rMbLFthAWRC6tgR38UEBWXogkizPkGUKhS',
          x('a87635e97fb76177a3a086efacd841a271b7e8d5'), 122,
          P2SHRavencoinAddress)

#        T('BC1QW508D6QEJXTDG4Y5R3ZARVARY0C5XW7KV8F3T4',
#          x('751e76e8199196d454941c45d1b3a323f1433bd6'), 0,
#          P2WPKHRavencoinAddress)

#        T('bc1qc7slrfxkknqcq2jevvvkdgvrt8080852dfjewde450xdlk4ugp7szw5tk9',
#          x('c7a1f1a4d6b4c1802a59631966a18359de779e8a6a65973735a3ccdfdabc407d'), 0,
#          P2WSHRavencoinAddress)

    def test_wrong_nVersion(self):
        """Creating a CRavencoinAddress from a unknown nVersion fails"""

        # tests run in mainnet, so both of the following should fail
        with self.assertRaises(CRavencoinAddressError):
            CRavencoinAddress('mpXwg4jMtRhuSpVq4xS3HFHmCmWp9NyGKt')

        with self.assertRaises(CRavencoinAddressError):
            CRavencoinAddress('2MyJKxYR2zNZZsZ39SgkCXWCfQtXKhnWSWq')

    def test_from_scriptPubKey(self):
        def T(hex_scriptpubkey, expected_str_address, expected_class):
            scriptPubKey = CScript(x(hex_scriptpubkey))
            addr = CRavencoinAddress.from_scriptPubKey(scriptPubKey)
            self.assertEqual(str(addr), expected_str_address)
            self.assertEqual(addr.__class__, expected_class)

        T('a914000000000000000000000000000000000000000087', 'r6Eb8FN9d1Xtmt1ZzBdtAJCynYS5jpWCRq',
          P2SHRavencoinAddress)
        T('76a914000000000000000000000000000000000000000088ac', 'R9HC5WtHbpoa51NCUAz86XLCmGTbkf45NT',
          P2PKHRavencoinAddress)
#        T('0014751e76e8199196d454941c45d1b3a323f1433bd6',
#          'bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4',
#          P2WPKHRavencoinAddress)
#        T('0020c7a1f1a4d6b4c1802a59631966a18359de779e8a6a65973735a3ccdfdabc407d',
#          'bc1qc7slrfxkknqcq2jevvvkdgvrt8080852dfjewde450xdlk4ugp7szw5tk9',
#          P2WSHRavencoinAddress)

    def test_from_nonstd_scriptPubKey(self):
        """CRavencoinAddress.from_scriptPubKey() with non-standard scriptPubKeys"""

        # Bad P2SH scriptPubKeys

        # non-canonical pushdata
        scriptPubKey = CScript(x('a94c14000000000000000000000000000000000000000087'))
        with self.assertRaises(CRavencoinAddressError):
            CRavencoinAddress.from_scriptPubKey(scriptPubKey)

        # Bad P2PKH scriptPubKeys

        # Missing a byte
        scriptPubKey = CScript(x('76a914000000000000000000000000000000000000000088'))
        with self.assertRaises(CRavencoinAddressError):
            CRavencoinAddress.from_scriptPubKey(scriptPubKey)

        # One extra byte
        scriptPubKey = CScript(x('76a914000000000000000000000000000000000000000088acac'))
        with self.assertRaises(CRavencoinAddressError):
            CRavencoinAddress.from_scriptPubKey(scriptPubKey)

        # One byte changed
        scriptPubKey = CScript(x('76a914000000000000000000000000000000000000000088ad'))
        with self.assertRaises(CRavencoinAddressError):
            CRavencoinAddress.from_scriptPubKey(scriptPubKey)

    def test_from_invalid_scriptPubKey(self):
        """CRavencoinAddress.from_scriptPubKey() with invalid scriptPubKeys"""

        # We should raise a CRavencoinAddressError, not any other type of error

        # Truncated P2SH
        scriptPubKey = CScript(x('a91400000000000000000000000000000000000000'))
        with self.assertRaises(CRavencoinAddressError):
            CRavencoinAddress.from_scriptPubKey(scriptPubKey)

        # Truncated P2PKH
        scriptPubKey = CScript(x('76a91400000000000000000000000000000000000000'))
        with self.assertRaises(CRavencoinAddressError):
            CRavencoinAddress.from_scriptPubKey(scriptPubKey)

    def test_to_redeemScript(self):
        def T(str_addr, expected_scriptPubKey_hexbytes):
            addr = CRavencoinAddress(str_addr)

            actual_scriptPubKey = addr.to_redeemScript()
            self.assertEqual(b2x(actual_scriptPubKey),
                             expected_scriptPubKey_hexbytes)

        T('r6Eb8FN9d1Xtmt1ZzBdtAJCynYS5jpWCRq',
          'a914000000000000000000000000000000000000000087')

        T('R9HC5WtHbpoa51NCUAz86XLCmGTbkf45NT',
          '76a914000000000000000000000000000000000000000088ac')

#        T('bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4',
#          '76a914751e76e8199196d454941c45d1b3a323f1433bd688ac')

    def test_to_scriptPubKey(self):
        """CRavencoinAddress.to_scriptPubKey() works"""
        def T(str_addr, expected_scriptPubKey_hexbytes):
            addr = CRavencoinAddress(str_addr)

            actual_scriptPubKey = addr.to_scriptPubKey()
            self.assertEqual(b2x(actual_scriptPubKey), expected_scriptPubKey_hexbytes)

        T('r6Eb8FN9d1Xtmt1ZzBdtAJCynYS5jpWCRq',
          'a914000000000000000000000000000000000000000087')

        T('R9HC5WtHbpoa51NCUAz86XLCmGTbkf45NT',
          '76a914000000000000000000000000000000000000000088ac')


class Test_P2SHRavencoinAddress(unittest.TestCase):
    def test_from_redeemScript(self):
        def T(script, expected_str_address):
            addr = P2SHRavencoinAddress.from_redeemScript(script)
            self.assertEqual(str(addr), expected_str_address)

        T(CScript(), 'rNgi5iPXJfKYt65YnocubTpm9swCcJwLTY')
        T(CScript(x('76a914751e76e8199196d454941c45d1b3a323f1433bd688ac')),
          'rQy5KSWuzWQwK6ZGJ8wkwLGDb5oCh5FXog')


class Test_P2PKHRavencoinAddress(unittest.TestCase):
    def test_from_non_canonical_scriptPubKey(self):
        def T(hex_scriptpubkey, expected_str_address):
            scriptPubKey = CScript(x(hex_scriptpubkey))
            addr = P2PKHRavencoinAddress.from_scriptPubKey(scriptPubKey)
            self.assertEqual(str(addr), expected_str_address)

            # now test that CRavencoinAddressError is raised with accept_non_canonical_pushdata=False
            with self.assertRaises(CRavencoinAddressError):
                P2PKHRavencoinAddress.from_scriptPubKey(scriptPubKey, accept_non_canonical_pushdata=False)

        T('76a94c14000000000000000000000000000000000000000088ac', 'R9HC5WtHbpoa51NCUAz86XLCmGTbkf45NT')
        T('76a94d1400000000000000000000000000000000000000000088ac', 'R9HC5WtHbpoa51NCUAz86XLCmGTbkf45NT'),
        T('76a94e14000000000000000000000000000000000000000000000088ac', 'R9HC5WtHbpoa51NCUAz86XLCmGTbkf45NT')

        # make sure invalid scripts raise CRavencoinAddressError
        with self.assertRaises(CRavencoinAddressError):
            P2PKHRavencoinAddress.from_scriptPubKey(x('76a94c14'))

    def test_from_bare_checksig_scriptPubKey(self):
        def T(hex_scriptpubkey, expected_str_address):
            scriptPubKey = CScript(x(hex_scriptpubkey))
            addr = P2PKHRavencoinAddress.from_scriptPubKey(scriptPubKey)
            self.assertEqual(str(addr), expected_str_address)

            # now test that CRavencoinAddressError is raised with accept_non_canonical_pushdata=False
            with self.assertRaises(CRavencoinAddressError):
                P2PKHRavencoinAddress.from_scriptPubKey(scriptPubKey, accept_bare_checksig=False)

        # compressed
        T('21000000000000000000000000000000000000000000000000000000000000000000ac', 'RD6GgnrMpPaTSMn8vai6yiGA7mN4QGPVMY')

        # uncompressed
        T('410000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000ac', 'RYcSf1PAjycb31WBycYukQACU1iZP3hLS7')

        # non-canonical encoding
        T('4c21000000000000000000000000000000000000000000000000000000000000000000ac', 'RD6GgnrMpPaTSMn8vai6yiGA7mN4QGPVMY')

        # odd-lengths are *not* accepted
        with self.assertRaises(CRavencoinAddressError):
            P2PKHRavencoinAddress.from_scriptPubKey(x('2200000000000000000000000000000000000000000000000000000000000000000000ac'))

    def test_from_valid_pubkey(self):
        """Create P2PKHRavencoinAddress's from valid pubkeys"""

        def T(pubkey, expected_str_addr):
            addr = P2PKHRavencoinAddress.from_pubkey(pubkey)
            self.assertEqual(str(addr), expected_str_addr)

        T(x('03d9e529a03f92beba94c85dd869f94388c19c6d7b7c055b3202fee0f70fbfd835'),
          'RL5dKQv7ZZYrqSYXNVgy2HvncjcQf8G6at')
        T(x('03172ea8a57b4c85a2721317d6f99f2d0bfbd624b2faaf465afde6fb7f8bc6a38a'),
          'RRHzVuPMUe3r9EhRWUusx5sBKn29SJ93UC')

        T(CPubKey(x('029ef231f0606dc7b9b4c7af16d0f4a9645b62564f6f167d1f053964b7efff6466')),
          'RBmjeJotJSH4mTJpiSj6eQK2kjDEhbRDBm')
        T(CPubKey(x('02b1f5646f25ecda92bcbd0bf819e1f97b2a61ebad9adfade85cec8bcdc00a2fbf')),
          'RLtrHG4X4BbipE4QkqnS16A5uLQt9dxqxp')

    def test_from_invalid_pubkeys(self):
        """Create P2PKHRavencoinAddress's from invalid pubkeys"""

        # first test with accept_invalid=True
        def T(invalid_pubkey, expected_str_addr):
            addr = P2PKHRavencoinAddress.from_pubkey(invalid_pubkey, accept_invalid=True)
            self.assertEqual(str(addr), expected_str_addr)

        T(x(''),
          'RRjK2yufHUbEBDSBGny9Xgwz8bxiWBC3m7')
        T(x('0378d430274f8c5ec1321338151e9f27f4c676a008bdf8638d07c0b6be9ab35c72'),
          'RURg8tQsyiNSQkDQWxjbDDDSJby1qkt5cf')

        # With accept_invalid=False we should get CRavencoinAddressError's
        with self.assertRaises(CRavencoinAddressError):
            P2PKHRavencoinAddress.from_pubkey(x(''))
        with self.assertRaises(CRavencoinAddressError):
            P2PKHRavencoinAddress.from_pubkey(x('0378d430274f8c5ec1321338151e9f27f4c676a008bdf8638d07c0b6be9ab35c72'))
        with self.assertRaises(CRavencoinAddressError):
            P2PKHRavencoinAddress.from_pubkey(CPubKey(x('0378d430274f8c5ec1321338151e9f27f4c676a008bdf8638d07c0b6be9ab35c72')))

class Test_CRavencoinSecret(unittest.TestCase):
    def test(self):
        def T(base58_privkey, expected_hex_pubkey, expected_is_compressed_value):
            key = CRavencoinSecret(base58_privkey)
            self.assertEqual(b2x(key.pub), expected_hex_pubkey)
            self.assertEqual(key.is_compressed, expected_is_compressed_value)

        T('5KJvsngHeMpm884wtkJNzQGaCErckhHJBGFsvd3VyK5qMZXj3hS',
          '0478d430274f8c5ec1321338151e9f27f4c676a008bdf8638d07c0b6be9ab35c71a1518063243acd4dfe96b66e3f2ec8013c8e072cd09b3834a19f81f659cc3455',
          False)
        T('L3p8oAcQTtuokSCRHQ7i4MhjWc9zornvpJLfmg62sYpLRJF9woSu',
          '0378d430274f8c5ec1321338151e9f27f4c676a008bdf8638d07c0b6be9ab35c71',
          True)

    def test_sign(self):
        key = CRavencoinSecret('5KJvsngHeMpm884wtkJNzQGaCErckhHJBGFsvd3VyK5qMZXj3hS')
        hash = b'\x00' * 32
        sig = key.sign(hash)

        # Check a valid signature
        self.assertTrue(key.pub.verify(hash, sig))
        self.assertTrue(IsLowDERSignature(sig))

        # Check that invalid hash returns false
        self.assertFalse(key.pub.verify(b'\xFF'*32, sig))

        # Check that invalid signature returns false.
        #
        # Note the one-in-four-billion chance of a false positive :)
        self.assertFalse(key.pub.verify(hash, sig[0:-4] + b'\x00\x00\x00\x00'))

    def test_sign_invalid_hash(self):
        key = CRavencoinSecret('5KJvsngHeMpm884wtkJNzQGaCErckhHJBGFsvd3VyK5qMZXj3hS')
        with self.assertRaises(TypeError):
          sig = key.sign('0' * 32)

        hash = b'\x00' * 32
        with self.assertRaises(ValueError):
          sig = key.sign(hash[0:-2])


class Test_RFC6979(unittest.TestCase):
    def test(self):
        if not is_libsec256k1_available():
            return

        use_libsecp256k1_for_signing(True)

        # Test Vectors for RFC 6979 ECDSA, secp256k1, SHA-256
        # (private key, message, expected k, expected signature)
        test_vectors = [
            (0x1, "Satoshi Nakamoto", 0x8F8A276C19F4149656B280621E358CCE24F5F52542772691EE69063B74F15D15, "934b1ea10a4b3c1757e2b0c017d0b6143ce3c9a7e6a4a49860d7a6ab210ee3d82442ce9d2b916064108014783e923ec36b49743e2ffa1c4496f01a512aafd9e5"),
            (0x1, "All those moments will be lost in time, like tears in rain. Time to die...", 0x38AA22D72376B4DBC472E06C3BA403EE0A394DA63FC58D88686C611ABA98D6B3, "8600dbd41e348fe5c9465ab92d23e3db8b98b873beecd930736488696438cb6b547fe64427496db33bf66019dacbf0039c04199abb0122918601db38a72cfc21"),
            (0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364140, "Satoshi Nakamoto", 0x33A19B60E25FB6F4435AF53A3D42D493644827367E6453928554F43E49AA6F90, "fd567d121db66e382991534ada77a6bd3106f0a1098c231e47993447cd6af2d06b39cd0eb1bc8603e159ef5c20a5c8ad685a45b06ce9bebed3f153d10d93bed5"),
            (0xf8b8af8ce3c7cca5e300d33939540c10d45ce001b8f252bfbc57ba0342904181, "Alan Turing", 0x525A82B70E67874398067543FD84C83D30C175FDC45FDEEE082FE13B1D7CFDF1, "7063ae83e7f62bbb171798131b4a0564b956930092b33b07b395615d9ec7e15c58dfcc1e00a35e1572f366ffe34ba0fc47db1e7189759b9fb233c5b05ab388ea"),
            (0xe91671c46231f833a6406ccbea0e3e392c76c167bac1cb013f6f1013980455c2, "There is a computer disease that anybody who works with computers knows about. It's a very serious disease and it interferes completely with the work. The trouble with computers is that you 'play' with them!", 0x1F4B84C23A86A221D233F2521BE018D9318639D5B8BBD6374A8A59232D16AD3D, "b552edd27580141f3b2a5463048cb7cd3e047b97c9f98076c32dbdf85a68718b279fa72dd19bfae05577e06c7c0c1900c371fcd5893f7e1d56a37d30174671f6")
        ]
        for vector in test_vectors:
            secret = CRavencoinSecret.from_secret_bytes(x('{:064x}'.format(vector[0])))
            encoded_sig = secret.sign(hashlib.sha256(vector[1].encode('utf8')).digest())

            assert(encoded_sig[0] == 0x30)
            assert(encoded_sig[1] == len(encoded_sig)-2)
            assert(encoded_sig[2] == 0x02)

            rlen = encoded_sig[3]
            rpos = 4
            assert(rlen in (32, 33))

            if rlen == 33:
                assert(encoded_sig[rpos] == 0)
                rpos += 1
                rlen -= 1

            rval = encoded_sig[rpos:rpos+rlen]
            spos = rpos+rlen
            assert(encoded_sig[spos] == 0x02)

            spos += 1
            slen = encoded_sig[spos]
            assert(slen in (32, 33))

            spos += 1
            if slen == 33:
                assert(encoded_sig[spos] == 0)
                spos += 1
                slen -= 1

            sval = encoded_sig[spos:spos+slen]
            sig = b2x(rval + sval)
            assert(str(sig) == vector[3])

        use_libsecp256k1_for_signing(False)
