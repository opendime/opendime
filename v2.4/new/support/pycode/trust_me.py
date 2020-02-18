#!/usr/bin/env python
#
# Python 2&3 code to check we are a legit Opendime.
#
from __future__ import print_function
try:
    input = raw_input
    B2A = lambda x:x
    A2B = lambda x:x.encode('ascii')
except NameError:
    # Py3
    B2A = lambda x: str(x, 'ascii')
    A2B = lambda x: bytes(x, 'ascii')

import os, sys, json, time, subprocess
from collections import OrderedDict
from .shared import find_root
from .remote_package import load_remote_module
from hashlib import sha256
from binascii import a2b_hex, b2a_hex
from base64 import b64encode

# See: https://github.com/richardkiss/pycoin
load_remote_module('pycoin')
from pycoin.contrib import msg_signing as MS

ADV = lambda path, fn: os.path.join(path, 'advanced', fn)

def fail(msg):
    print("\n" + '*'*48)
    print("FAIL FAIL FAIL -- Do Not Trust -- FAIL FAIL FAIL")
    print('*'*48 + '\n')

    print('PROBLEM: ' + msg)
    sys.exit(1)

def lowlevel_tests(path, expect, expect_addr, version):
    # this requires: "pip install PyUSB" and a working libusb library
    try:
        import usb, usb.core
    except ImportError:
        print("\n(additional tests are possible with libusb and PyUSB installed)\n")
        return

    load_remote_module('ecdsa')

    print("\nAdditional low-level checks:")

    if hasattr(os, 'statvfs'):
        g = os.statvfs(path)
        try:
            assert g.f_frsize == 512
            assert 2800 <= g.f_blocks <= 2880
        except AssertionError:
            fail("os.statvfs didn't shown correct disk geometry")
        print("  - correct virtual disk geometry")

    class dev(object):
        def __init__(self, sn):
            self.dev = usb.core.find(idVendor=0xd13e, custom_match=lambda d:d.serial_number==sn)
            assert self.dev, "Was not able to find USB device!"

        def read(self, idx):
            return self.dev.ctrl_transfer(bmRequestType=0xc0, bRequest=0, wValue=idx,
                                    data_or_wLength=500).tostring()

        def write(self, cmd, data):
            self.dev.ctrl_transfer(bmRequestType=0x40, bRequest=0,
                                        wValue=ord(cmd), data_or_wLength=data)

    if 'sn' not in expect:
        # fresh v1, we don't know anything
        print("  - sorry this version cannot do more checks")
        return

    try:
        u = dev(expect['sn'])
        assert u.dev.serial_number == expect['sn'], "Serial number mismatch"
    except AssertionError:
        fail("Could not find device over low-level USB")


    if expect_addr:
        try:
            # version 1.0.0 will fail here
            addr = B2A(u.read(3))
        except:
            if version == '1.0.0':
                print("  - sorry this version cannot do more checks")
                return

        try:
            assert addr == expect['ad'].strip(), "Payment address mismatch"
            assert addr == expect_addr, "JSON vs address.txt mismatch"
        except AssertionError:
            fail('''\
    Low level USB details do not match the values observed at the filesystem level!
    ''')

        print("  - read-back over USB EP0 correct")

        for i in range(5):
            msg = B2A(b2a_hex(os.urandom(16)))
            u.write('m', msg)

            for retry in range(1000):
                try:
                    sig = B2A(b64encode(u.read(4)))
                    break
                except usb.core.USBError:
                    time.sleep(.010)
        
            ok = MS.verify_message(addr, sig, msg)
            if not ok:
                fail("Incorrect signature on test message!")
            else:
                print("  - good bitcoin message signing #%d: %s" % (i+1, msg[0:12]))

    if not version.startswith('2.'):
        print("  - version 2 device could be checked even more")
        return

    # test also Atmel EC508A cert + signature

    chain = ADV(path, 'chain.crt')
    unit = ADV(path, 'unit.crt')
    x = B2A(subprocess.check_output(['openssl', 'verify', '-CAfile', chain, unit ]))
    if not x.endswith('unit.crt: OK\n'):
        fail("Factory certificate failed verify by Openssl!")

    x = subprocess.check_output(['openssl', 'x509', '-in', chain, '-noout', '-fingerprint' ])
    if b'A1:02:01:E3:02:0E:C9:6B:30:90:62:69:CD:E3:6F:82:80:35:A9:8B' not in x:
        fail("Factory certificate is wrong.")

    x = subprocess.check_output(['openssl', 'x509', '-in', unit, '-noout', '-subject' ])
    print(x)
    list = B2A(x).split(',')
    print("list:")
    print(list)
    print("subj:")
    subj = list[0]
    print(subj)
    print("expected data:")
    print(expect)
    expected_string = 'subject=serialNumber = "' + expect['sn'] + '+' + expect['ae'] + '"'
    print("expected string:")
    print(expected_string)
    if subj != expected_string:
        fail("Certificate is for some other unit: " + subj)

    print("  - genuine per-unit factory certificate verified")

    from ecdsa import VerifyingKey

    x = subprocess.check_output(['openssl', 'x509', '-in', unit, '-noout', '-pubkey' ])
    pubkey = VerifyingKey.from_pem(B2A(x))

    for i in range(5):
        numin = os.urandom(20)
        u.write('f', numin)

        for retry in range(1000):
            try:
                resp = u.read(4)
                break
            except usb.core.USBError:
                time.sleep(.010)
                resp = None

        if not resp:
            fail("Didn't accept sign request")
    
        sig = resp[0:64]
        ae_rand = resp[64:]

        ok = verify_ae_signature(pubkey, expect, numin, ae_rand, sig)
        if not ok:
            fail("Incorrect signature in anti-counterfeiting test!")
        else:
            print("  - good anti-counterfeiting test #%d: %s" % (i+1, B2A(b2a_hex(numin))[0:12]))

def verify_ae_signature(pubkey, expect, numin, ae_rand, sig):
    H = lambda x: sha256(x).digest()

    if 'ad' in expect:
        slot13 = A2B(expect['ad'].ljust(72))[0:32]
        lock = b'\0'
    else:
        slot13 = b'\xff' * 32
        lock = b'\1'

    slot14 = A2B(expect['sn'] + "+" + expect['ae'])[0:32]

    fixed = b'\x00\xEE\x01\x23' + b'\0' *25
    msg1 = slot14 + b'\x15\x02\x0e' + fixed + H(ae_rand + numin + b'\x16\0\0')
    msg2 = slot13 + b'\x15\x02\x0d' + fixed + H(msg1)
    SN = a2b_hex(expect['ae'])

    body = H(msg2) + b'\x41\x40\x00\x00\x00\x00\x3c\x00\x2d\0\0\xEE' \
                + SN[2:6] + b'\x01\x23'+ SN[0:2] + lock + b'\0\0'

    from ecdsa.keys import BadSignatureError
    try:
        ok = pubkey.verify(sig, body, hashfunc=sha256)
    except BadSignatureError:
        ok = False

    return ok

        
def main():
    path = find_root()

    print("\nOpendime USB at: " + path)
    try:
        addr = open(os.path.join(path, 'address.txt')).read().strip()
        print("\n Wallet address: " + addr, end='\n\n')
        has_addr = True
    except IOError:
        has_addr = False

    vers = open(ADV(path, 'version.txt')).read().strip()
    dotted, details = vers.split(' ', 1)
    
    print("\nOpendime Version: " + dotted, end='\n\n')

    details = OrderedDict(p.split('=') for p in details.split(' '))
    try:
        vary = json.load(open(ADV(path, 'variables.json')))
        sn = vary['sn']
        if 'ae' in vary:
            sn += '+' + vary['ae']
        details['serial'] = sn
    except:
        if has_addr:
            fail("Unable to read variables.json?")
        vary = {}

    for k in details:
        print("  %8s: %s" % (k, details[k]))

    if 'INSECURE' in details:
        print("\n==> Insecure Version -- for demo/testing purposes only <==\n")

    if has_addr:
        msg = open(os.path.join(path, 'advanced', 'verify.txt')).read().strip()
        msg, sig_addr, sig = MS.parse_signed_message(msg)

        # force newlines to what we need.
        if '\r' not in msg:
            msg = msg.replace('\n', '\r\n')

        if sig_addr != addr:
            fail('''\
verify.txt message not signed by correct address for unit.

You would be sending funds to: %s
but this devices asserts knowledge of: %s''' % (addr, sig_addr))

        # do math to verify msg
        ok = MS.verify_message(addr, sig, msg)

        if not ok:
            fail('''Invalid or incorrectly-signed advanced/verify.txt found.''')

        # check contents make sense
        if vers not in msg:
            fail("Exact version string not found in verify message")


    lowlevel_tests(path, vary, sig_addr if has_addr else None, dotted)

    if has_addr and 'UNSEALED' in msg:
        fail('''Unsealed already.\n
This Opendime looks legit but has been "unsealed". Anyone might have the private key and access to the funds it may contain. Remove funds (if any) immediately and do not trust as payment.''')

    print("\nLooks good!\n\n" + (addr if has_addr else ''))
    
if __name__ == '__main__':
    main()
