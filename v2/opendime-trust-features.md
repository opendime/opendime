# DRAFT --- DRAFT --- DRAFT

# Opendime Version 2 Security Features

## How it works and why trust it

The latest generation of Opendime products include a new chip to 
make creating a counterfeit device impossible. 

This technical paper will explain the verification steps involving
the new chip and how it works.

For people who just want to verify a specific Opendime, you only
need to read the first section.

## Using the `trustme.py` program 

Each Opendime includes a python program which can be used to perform
all the verification steps. It is a simple command-line program
but does require a limited amount of setup.

### Setup Steps

You can verify an Opendime is genuine by following these steps:

1) Install [python](https://www.python.org/downloads/). For Linux and
MacOS users, it's already present and nothing needs to be done.
We support python2 and python3 so any recent version should work fine.

2) Install "libusb" so we can access USB devices directly. For MacOS,
these are the steps:

    - `brew install libusb`
    - `pip install PyUSB`

This step is optional, however, only the "light" verification of
the basics can be done. To check the new security chip, we need
`libUSB` because we need to communicate interactively with the Opendime
hardware. A small warning is shown if we can't do the extra checks.

3) Optional: install two python packages: `pycoin` and `ecdsa`. You can skip
this step because if you don't have them, the code will download
them as it runs, but that is slow and requires an Internet connection.

    - `pip install pycoin`
    - `pip install ecdsa`

We require version `0.76` or later for pycoin. Use `virtualenv`
if you have something older already installed.

4) Insert the Opendime device and run `trustme.py` from the `advanced` directory:

    - `cd /Volumes/OPENDIME/advanced`
    - `python trustme.py`

5) Wait and read the output of the program. It takes a few seconds
and prints progress as it runs.  If anything goes wrong, it prints a
large error message to attract your attention.

### Example Output

Here's what it will look like for a typical device (all of the
numbers will be different for your case, of course):

```
% cd /Volumes/OPENDIME/advanced
% ./trustme.py 

Opendime USB at: /Volumes/OPENDIME

 Wallet address: 1PBDnk9JdQ4ckwyM5RPMsULegYo8C8W7k4


Opendime Version: 2.0.0

      time: 20170201.135913
       git: v2@aef4015
    serial: SPX6ESSUJVGVCIBAEBDTMDAK74+2155ccbebab2


Additional low-level checks:
  - correct virtual disk geometry
  - read-back over USB EP0 correct
  - good bitcoin message signing #1: c9b3c2ee9de4
  - good bitcoin message signing #2: 40cb14243461
  - good bitcoin message signing #3: 466fd58993b7
  - good bitcoin message signing #4: f8f4ac812d77
  - good bitcoin message signing #5: 7275545eda5b
  - genuine per-unit factory certificate verified
  - good anti-counterfeiting test #1: de09f6fb2f71
  - good anti-counterfeiting test #2: db28500fa5b6
  - good anti-counterfeiting test #3: 41b6f551af3f
  - good anti-counterfeiting test #4: af23fa42e755
  - good anti-counterfeiting test #5: 773d46ebc8d3

Looks good!

1PBDnk9JdQ4ckwyM5RPMsULegYo8C8W7k4
```

### Cross-Device Verification

Since this code is running from inside the Opendime it is verifying,
it is irresponsible to trust what it says. You should **always** use
code from a trusted source to verify an untrusted Opendime.
Typically that would be the same file from another Opendime that
you know is good because you bought it.

To test between two units, provide the path to the *other* Opendime
as the first argument:

    - `python trustme.py /Volumes/OPENDIME\ 2`

If you don't have a trusted Opendime, you can checkout the code
from the [Opendime github repo](https://github.com/opendime/opendime)
and run directly from that checkout, under `v2/sealed/advanced/trustme.py`.
You must provide the path to USB drive as an argument.

We will also publish the SHA256 hashes for the non-changing contents
of the Opendime, and by checking `advanced/trustme.py` and
`support/pycode.zip` you can be confident that you are running the
unmodified python code.


### Manual Certificate Verification

Each v2 Opendime ships with a unique x.509 certificate. The certificate
contains the serial numbers (for both chips) and reveals the public key
used to sign challenges. The `trustme.py` program verifies the certificate,
but you can also do it manually as follows:

```
% cd /Volumes/OPENDIME/advanced

% openssl verify -CAfile chain.crt unit.crt
unit.crt: OK

% openssl x509 -in chain.crt -fingerprint -noout
SHA1 Fingerprint=A1:02:01:E3:02:0E:C9:6B:30:90:62:69:CD:E3:6F:82:80:35:A9:8B

% openssl x509 -in unit.crt -subject -noout
subject= /serialNumber=SPX6ESSUJVGVCIBAEBDTMDAK74+2155ccbebab2/CN=Opendime
```

It's important to check the fingerprint value of the `chain.crt`
file matches the above digits exactly. That's proof that the Coinkite
factory signed this unit's certificate. You should also check the
serial number matches your device. Perhaps you can see the USB
device serial number from your operating system somehow? (In this
example, that's SPX6ESSUJVGVCIBAEBDTMDAK74). The second part of the
serial number (after the plus) is the serial number laser-etched
into the ATECC508A.

The code in `trustme.py` does those checks, and most importantly,
gets the Opendime to sign a number of unique and complex messages
with the public key taken from the certificate. The signature responses
are verified against the public key confirmed by the certificate.


# Advanced Verification / How It Works

## Background

We use the [Atmel ATECC508A](http://www.atmel.com/devices/atecc508a.aspx)
to anchor our trust. To understand how it all works, we need to share a little
about the details of this chip and how we've applied it to our task.

(Unfortunately, the detailed datasheet is covered by an NDA, so we
cannot get into all the details.)

Chip features include:

- Crypto element device with secure hardware-based key storage
- Performs High-Speed Public Key Algorithms (PKI): ECDSA and ECDH
- NIST Standard P256 Elliptic Curve support. (It cannot do other curves.)
- SHA-256 hash algorithm implemented in hardware.
- Guaranteed unique 72-bit serial number, assigned by Atmel at the factory.
- Internal high-quality FIPS true Random Number Generator (TRNG)
- Storage for up to 16 private keys, and total memory of about 10kbits.

This chip is designed for private key storage, and is not a general
purpose micro. It has all the hardware features you would expect of
a key-storage chip. In particular, it has specific defenses against
inspection by electron-microscope and power analysis. 

There are numerous design features of the chip and it's protocol
that effectively force you into good security design to be able to
use it. For example, you cannot load any keys onto the chip until
the usage, rights and settings of all key slots is defined and set
in stone.  Many state transitions are strictly one-way, and of
course, there are trapdoors that allow write but provide no means
to read back values.

For the critical EC (Elliptic Curve) private key, we actually
generate it internal to the device and it never leaves the chip.
Even the Coinkite factory, where all Opendimes are born, does not
know that key's value. We only know the public key for it, the same
as you! There are no commands to read out private keys, regardless
of authentication steps beforehand. Even the hashing of secret
values is controlled in a number of clever ways that assure you
cannot deduce the contents of sensitive areas by asking for digests.


## Flash memory contents of Security Chip

The security chip is external to the main micro, so it can only
atest to facts that are stored in it's own flash memory. For that
reason, we store the following things in the security chip:

- the private EC key documented in the certificate (`unit.crt`)
- the pairing secret (256 bits)
- a copy of the serial number of main micro
- a copy of bitcoin address for the Opendime, once it is picked
- a copy of the public key which matches the certificate

The Bitcoin address is only programmed after the user has
provided entropy and the Opendime picks the secret exponent
and matching Bitcoin public key hash. It is stored in Base58
and is the only part of the chip that can change after it
leaves our factory.

## Pairing Secret

When the factory makes a new Opendime, we create a completely random
pairing secret (256 bits) and put that shared secret into both the
main micro and the security chip. That pairing secret is intended
to prevent moving the Atmel 508A between different boards.

To demonstrate both chips are paired correctly, on each boot up,
the main micro does an challenge/response sequence involving this
shared secret. Both the micro and the ATECC508A both add randomness
to this exchange so there is no way to replay the challenge sequence,
and the keys involved are unique to each Opendime/ATECC508A pair
anyway.

The pairing secret is also linked into the EC private key used for
signing. To be able to sign a challenge with the main secret EC
key, the main micro must successfully complete the pairing-key secret
challenge. This policy is enforced by hardware inside the ATECC508A.

Of course, the main micro will also refuse to work if the challenge
fails during boot up. For this reason, if you remove the ATECC508A
from an Opendime, it will not boot anymore. (Aside: If you break
the seal on an Opendime in that state, you should still be able to
extract your funds, but you'll have to connect a serial port to
certain pins and there are no guarantees.)

The crypto steps for the pairing challenge are as follows:

- pick 20-byte random nonce (160 bits)
- send that to ATECC508A ("num_in")
- read back a 32-byte nonce generated by the TRNG of the ATECC508A ("rndout")
- calculate: temp = SHA256(rndout + num_in + constants)
- pick another 13-bytes of nonce ("otherdata")
- calculate: response = SHA256(pairing_secret + temp + otherdata + constants)
- send that to ATECC508A chip, and expect yes/no response
- check that private key is now unlocked for signing purposes

This sequence is documented publicly in the datasheet for the
[ATSHA204A](http://www.atmel.com/products/security-ics/cryptoauthentication/sha-256.aspx)
which is a simpler, non-EC version of the 508A. Look
at the descriptions for the `Nonce` and `CheckMAC` commands respectively.

## Background on the Certificate Chain

After some research into alternatives, we chose traditional x.509
certificates for this project. The advantage is we can use OpenSSL
and similar commonly-deployed tools for verification of those
certificates.  In an ideal world, we could use EC crypto for the
certificates, but we have found many compatibility problems with
OpenSSL and EC keys.  Therefore, our certificate chain uses DSA
keys except at the leaf level which is EC. For this project, we are
forced to use a NIST curve and that curve is supported nicely in
ASN.1/x.509 certificates.

As proposed by **Theymos** in a
[Reddit comment](https://www.reddit.com/r/Bitcoin/comments/5kkgth/announcing_opendime_v2_now_genuine_verified/dbp44xi/)
we are using a two-level hierarchy. There is a "factory key" which
we keep offline and use only to sign a lower-level "batch key" one
time. The batch key is used to sign each unit's public key.

You and your software should use the fingerprint of our factory key
and verify the certificate chain from the unit's own certificate
back to the factory key. Please do not assume we won't be making
more batch certificates in the future!

Here is a dump of the certificate chain, which we include in the
file: `advanced/chain.crt`. Please note there are two concatenated
certificates in that file as it was designed for use with the
`openssl verify` command as the `-CAfile` argument.

```
% openssl x509 -noout -text -in factory-root-1.crt
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number: 1 (0x1)
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: C=CA, ST=Ontario, L=Toronto, O=Coinkite Inc., OU=Opendime, CN=Factory Root CA 1
        Validity
            Not Before: Feb  1 00:00:00 2017 GMT
            Not After : Jan  1 00:00:00 2037 GMT
        Subject: C=CA, ST=Ontario, L=Toronto, O=Coinkite Inc., OU=Opendime, CN=Factory Root CA 1
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
            RSA Public Key: (2048 bit)
                Modulus (2048 bit):
                    00:c2:b0:d8:e8:de:a4:3c:31:ca:a4:06:66:48:79:
                    d7:df:ac:9c:c1:f3:23:57:91:ea:fa:ce:22:76:8a:
                    0e:6a:b6:b1:34:04:e7:1e:4f:32:83:5d:58:4a:7a:
                    7f:45:75:2f:97:b9:60:07:d5:7d:ac:ee:e4:bf:dd:
                    d8:64:03:23:62:48:b0:24:06:3f:bb:d8:92:a9:06:
                    7c:54:40:bf:35:8f:32:23:6b:c0:d9:0f:43:29:8f:
                    14:2e:4f:fb:6a:d1:c4:09:3e:5b:d9:93:a6:30:34:
                    a1:9e:97:a7:9f:81:e6:85:93:ba:51:98:ca:03:e5:
                    78:ee:96:c7:12:af:c4:61:1c:0f:45:8e:65:0a:83:
                    98:84:55:21:c0:83:d4:38:84:1e:a0:d6:98:7c:d1:
                    3b:ac:94:68:7a:cc:df:6d:e2:47:ff:11:ae:45:52:
                    9f:6f:3c:bd:c3:94:38:77:b7:70:6f:4b:49:66:8c:
                    c0:10:7e:06:d7:32:28:62:5f:8b:c7:ee:75:24:1d:
                    49:04:bb:e4:79:33:9c:52:2c:d8:4e:9f:da:d8:da:
                    e3:62:e6:2f:e1:37:ec:57:ed:71:b6:80:2f:cc:af:
                    93:98:6a:03:c3:d6:be:46:7f:d4:5a:23:48:97:a1:
                    02:e3:1a:fe:c1:ea:44:4d:63:74:97:86:e2:30:82:
                    dd:cf
                Exponent: 65537 (0x10001)
        X509v3 extensions:
            X509v3 Basic Constraints: critical
                CA:TRUE
            X509v3 Subject Key Identifier: 
                34:4C:11:65:52:33:76:7A:D6:38:53:F0:D4:1F:AF:4D:66:40:60:E8
            X509v3 Key Usage: critical
                Certificate Sign, CRL Sign
    Signature Algorithm: sha256WithRSAEncryption
        b4:87:e6:b6:dc:dd:20:4d:02:8c:63:bc:02:4c:63:ec:9e:ea:
        4e:91:d0:3d:7d:d2:fc:8d:2a:09:17:5b:07:06:80:ed:9d:fb:
        64:c3:de:c5:2b:e3:49:ed:6b:e5:d2:08:35:3b:dc:22:1f:25:
        3e:8f:67:cf:e0:ce:a4:e6:21:7e:47:c7:20:df:98:c5:35:e9:
        0c:36:2c:db:47:e1:32:f0:b9:e9:f2:44:7d:7e:7d:6d:37:36:
        52:d9:49:5a:11:7e:a4:f4:41:96:16:f1:2a:e0:f2:f8:ad:2b:
        db:cf:b4:52:48:2a:20:43:8c:7b:ff:9b:c6:16:32:98:56:5b:
        80:09:5a:75:17:89:d8:bb:39:41:f3:b7:b0:04:7f:6a:53:cd:
        b5:cb:fd:d8:71:d6:c1:76:a6:fe:53:f1:0a:d7:f2:54:d6:4d:
        bd:46:2b:60:36:38:34:00:5b:b6:62:3d:5f:a2:21:a5:72:35:
        a0:33:12:66:4e:b9:5b:a0:99:5a:97:e6:9d:41:8e:86:d5:fe:
        ef:68:3f:38:86:71:ec:44:f9:e5:24:09:0d:42:be:57:6a:79:
        f3:4e:bc:70:65:94:2e:d2:80:30:89:d8:5e:69:33:14:12:21:
        83:31:11:82:3e:16:2f:98:ff:03:b1:ab:19:c2:27:cf:13:91:
        4d:06:2e:74



% openssl x509 -noout -text -in batch-01.crt 
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number: 1001 (0x3e9)
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: C=CA, ST=Ontario, L=Toronto, O=Coinkite Inc., OU=Opendime, CN=Factory Root CA 1
        Validity
            Not Before: Feb  1 00:00:00 2017 GMT
            Not After : Jan  1 00:00:00 2037 GMT
        Subject: CN=Batch #1 CA
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
            RSA Public Key: (2048 bit)
                Modulus (2048 bit):
                    00:b9:49:6d:84:fa:0b:5d:f1:67:9d:b6:b7:2b:22:
                    27:b5:b5:fd:6e:9b:6f:69:cc:db:a7:16:ac:38:e4:
                    07:7f:2f:9d:c2:4e:ec:12:c2:16:4d:27:86:ad:61:
                    8b:32:36:51:ea:f4:c7:ae:79:a6:40:bf:c2:1b:88:
                    c3:5f:98:cb:3e:0c:3b:6b:b0:71:48:1d:12:94:8d:
                    04:2a:97:63:e7:7a:af:c8:e5:e5:66:f3:7d:a1:af:
                    7e:4f:62:50:a6:ae:f3:55:30:3d:43:17:fe:b4:ad:
                    3f:fe:49:fe:52:b0:3e:23:5e:8a:94:55:6a:7d:8f:
                    60:ba:85:df:9a:d2:17:ab:b5:50:44:61:e3:79:88:
                    cd:e7:ff:6b:87:c7:58:25:56:ab:f2:51:88:dd:b7:
                    5f:75:62:2c:63:2e:16:89:56:18:1a:81:20:50:fc:
                    f1:ff:f0:ac:30:0b:38:2c:4e:60:93:90:ec:63:2c:
                    71:75:0f:c9:89:6a:7e:70:6c:dc:85:c0:44:ea:ad:
                    c1:08:8f:94:14:90:54:74:b0:a2:d9:df:1b:bb:cc:
                    f6:2a:cd:3b:a0:2d:69:76:17:09:ca:fa:0f:61:f4:
                    87:d2:8d:1f:19:ec:7c:e1:c5:c4:85:c9:92:87:e0:
                    d0:92:2c:5f:8a:ab:a3:b6:2c:ad:12:b9:eb:ac:c8:
                    4a:fd
                Exponent: 65537 (0x10001)
        X509v3 extensions:
            X509v3 Authority Key Identifier: 
                keyid:34:4C:11:65:52:33:76:7A:D6:38:53:F0:D4:1F:AF:4D:66:40:60:E8

```

We haven't decided yet how big the "batches" will be. There may
be thousands of units in each batch.

Each unit will ship with a unique certificate that is signed by the
batch certificate from the `chain.crt` file.  The subject for this
"unit" certificate includes the serial number for the main micro
and the ATECC508A chip.

Here is the `advanced/unit.crt` decoded for an example unit.

```
openssl x509 -noout -text -in /Volumes/OPENDIME/advanced/unit.crt 
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            29:a1:3b:b4:12:d6:df:1f
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: CN=Batch #1 CA
        Validity
            Not Before: Feb  1 00:00:00 2017 GMT
            Not After : Jan  1 00:00:00 2037 GMT
        Subject: serialNumber=5NXBX5CUJVGVCIBAEBDTSGYK74+b134e591d2ba, CN=Opendime
        Subject Public Key Info:
            Public Key Algorithm: id-ecPublicKey
            EC Public Key:
                pub: 
                    04:9d:8b:8e:11:70:63:6a:db:7c:da:c9:a6:7f:36:
                    c3:b8:3a:72:a2:40:2a:0b:07:22:25:38:b2:6f:c9:
                    ad:d4:58:9d:06:00:e4:f0:3f:af:8e:21:b2:1f:98:
                    2b:eb:77:bd:7c:73:fc:e3:37:a9:ec:9c:f6:a1:68:
                    17:5d:43:2b:93
                ASN1 OID: prime256v1
        X509v3 extensions:
            X509v3 Authority Key Identifier: 
                keyid:9D:85:56:62:46:0C:56:01:9C:E7:D8:5D:47:F9:34:4D:A1:B7:C8:90

            X509v3 Basic Constraints: 
                CA:FALSE
            X509v3 Subject Key Identifier: 
                C6:00:4A:1F:20:9B:AF:C8:C6:70:DA:E8:E8:C7:40:4B:C9:B3:AE:4A
            X509v3 Key Usage: critical
                Digital Signature
    Signature Algorithm: sha256WithRSAEncryption
        53:ec:01:9d:a4:12:75:39:67:40:4b:d4:45:54:29:0f:47:06:
        22:98:37:b6:b4:b8:4e:55:1a:28:73:06:4b:0d:fb:68:75:e0:
        e6:27:67:8b:e9:b5:f2:ef:89:5b:28:91:24:03:3a:9e:d9:a2:
        43:2f:60:cd:a1:66:08:a4:b3:e7:27:36:96:f8:7c:ed:83:d6:
        73:fa:28:88:2f:de:21:a0:c0:7d:29:8c:53:c1:83:23:0b:f1:
        3c:fc:a7:42:92:27:f8:de:44:7f:79:93:21:62:b7:8e:4b:3f:
        36:bb:ab:eb:9b:8f:1c:0a:ed:df:1f:e6:ee:c2:51:25:19:e3:
        2a:61:15:6f:8a:4f:85:43:e4:45:fd:35:45:8c:d5:ee:77:27:
        5a:a8:e1:29:b3:da:15:f2:6c:fb:50:54:91:5b:74:35:57:f0:
        9a:30:d0:5d:bb:1c:69:ee:9e:01:5c:87:96:c9:68:e7:9e:f7:
        d2:41:7c:71:0f:73:23:c7:c5:91:01:d4:82:3f:bb:33:20:60:
        f6:22:1c:2f:73:bd:c2:43:c9:d7:0b:a2:95:42:9a:92:d3:1b:
        a9:a6:e5:e5:12:c4:17:70:64:ee:cf:b2:3b:8a:d7:ef:77:a2:
        84:db:3f:4b:eb:8c:a7:bf:d9:47:6b:cf:d7:57:f2:72:82:80:
        c0:79:31:d7
```

To extract the public key for verification purposes, you can use
this command:

```
% openssl x509 -noout -in /Volumes/OPENDIME/advanced/unit.crt -pubkey
-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEnYuOEXBjatt82smmfzbDuDpyokAq
CwciJTiyb8mt1FidBgDk8D+vjiGyH5gr63e9fHP84zep7Jz2oWgXXUMrkw==
-----END PUBLIC KEY-----
```

The result is a PEM-encoded public key, with the curve name included.

```
% openssl x509 -noout -in /Volumes/OPENDIME/advanced/unit.crt -pubkey | openssl asn1parse
    0:d=0  hl=2 l=  89 cons: SEQUENCE          
    2:d=1  hl=2 l=  19 cons: SEQUENCE          
    4:d=2  hl=2 l=   7 prim: OBJECT            :id-ecPublicKey
   13:d=2  hl=2 l=   8 prim: OBJECT            :prime256v1
   23:d=1  hl=2 l=  66 prim: BIT STRING        
```

## Signing Details

With the EC public key shared in the certificate, and now traced
back to the factory by the x.509 certificate chain, we just need a
signature to verify. The signature is created internally to the
ATECC508A, and starts with a nonce.

We implement a vendor-specific request on USB endpoint zero for
this purpose. If you write 20 bytes of nonce to that request
(called "numin"), you will receive back a
64-byte signature (X, Y values, raw, no DER encoding) and
32-bytes of random nonce that was
picked by the ATECC508A. (If you are interested in the USB protocol
details, see `trust_me.py` inside `advanced/pycode.zip`.)

The 20 bytes of "numin" are mixed with the nonce picked by the chip.
This creates the first digest. That is then hashed with main micro's
serial number and then that hash is hashed with the Opendime bitcoin
address (or ones if it doesn't have one yet). Finally, that hash
is combined with the serial number number of the ATECC508A, along
with a number of internal configuration values which effectively
atest to the configuration of the chip itself.

That sounds very simple, but the details matter critically and you
must construct the message for hashing yourself---the chip does not
provide it, nor any part of it. Each and every bit must be correct
for the signature to verify.

Here is some example code that can generate the message body needed.
Note that `variables` is a dictionary with key `ae` to hold the
serial number of the ATECC508A (in hex) and `sn` for the main micro's
serial number (in Base32). If the unit has picked a Bitcoin address,
then it will be present as key value `ad` (in Base58).

```python
def message_to_be_signed(variables, numin, ae_rand):
    H = lambda x: sha256(x).digest()

    if 'ad' in variables:
        slot13 = A2B(variables['ad'].ljust(72))[0:32]
        lock = b'\0'
    else:
        slot13 = b'\xff' * 32
        lock = b'\1'

    slot14 = A2B(variables['sn'] + "+" + variables['ae'])[0:32]

    fixed = b'\x00\xEE\x01\x23' + b'\0' *25
    msg1 = slot14 + b'\x15\x02\x0e' + fixed + H(ae_rand + numin + b'\x16\0\0')
    msg2 = slot13 + b'\x15\x02\x0d' + fixed + H(msg1)
    SN = a2b_hex(variables['ae'])

    return H(msg2) + b'\x41\x40\x00\x00\x00\x00\x3c\x00\x2d\0\0\xEE' \
                + SN[2:6] + b'\x01\x23'+ SN[0:2] + lock + b'\0\0'
```

There are many fixed values in the above. Most correspond to
command/configuration values of the ATECC508A and a few are just
padding.  With access to the full datasheet, you can see the chip
designers have carefully included any and all configuration values
that would be useful to bypass. Because those config values are
captured into the signature, you can be assured the chip is configured
in a secure manner as required for this application.


## Examining the Python Code

If you'd like to view the python code in `trustme.py`, you can unpack it as follows:

```
% mkdir unpacked
% cd unpacked
% cp /Volumes/OPENDIME/advanced/trustme.py .
% unzip /Volumes/OPENDIME/support/pycode.zip
% python ./trustme.py
(to show it still works)
% vi pycode/trust_me.py
```


## Q and A

#### Is the bitcoin private key holding funds stored in the ATECC508A?

- No. We do not store that in the ATECC508A. We felt it was too
difficult to move it securely between the two chips, and we worried
about reducing the reliability of the overall system.

#### Can I verify the device before it picks a key?

- Yes. In V2 of Opendime, the `trustme.py` program is available and
works on factory-fresh Opendimes. In fact, it makes a lot of sense
to verify the board is genuine before it picks the (Bitcoin) private key.

#### What if someone cracks the main micro?

- The attacker could still not clone the Opendime because the pairing
key and serial numbers would be different on all other boards. The
attackers cannot create a new certificate (because they don't have
access to our factory key).  They would not be able to make the
ATECC508A on that board lie about anything (such as bitcoin address)
because the memory of that chip is write-once and the signature
covers the values they would want to modify.

#### What if someone cracks the ATECC508A chip?

- Without also cracking the main micro, nothing is gained. Even if
they could read out all the secret values, they would gain only the
pairing secret and private key for a single Opendime. It gives them
nothing useful for other units.

#### What if the attackers completely replaced the main micro firmware?

- This can be done without cracking any security; security features
allow the main micro to be erased completely and then new firmware
could be developed from scratch. However, since the ATECC508A cannot
be copied, nor new ones made (without the factory keys to sign the
certificates), it would not be possible to create firmware that
passes verification.

#### Could an agency force you to clone an existing Opendime?

- Because the private key of the ATECC508A is not known to the
factory, we cannot produce or even emulate a specific chip. The
serial number is also out of our control (set by Atmel) and forms
part of the signature. This means it is impossible for us to exactly
clone an Opendime. We can only make new original ones.

#### What if I mess with voltages during the unseal process?

- One might attempt this to get the Opendime to reveal the private
key without fully making the transition to unsealed state. We avoid
this possibility by carefully choosing the value and location of
the byte in flash which is used to indicate if the unit is "sealed".
The firmware starts this value at `0xff` when it has no private key
set. Once a private key is picked (entering sealed state) it is
changed to `0x55`. When we unseal, it is set to `0x00` and verified
as zero before proceeding. Any unexpected value in this byte will
cause a transition to unsealed state (and clear the remaining bits).
Our chip has typical NOR flash logic, so a "page erase" is the only
way to set bits to one (but it's easy to set them to zero). There
is no simple way to make those zero bits one again: you'd need to
erase 64 bytes and then set just the right four of them to zero
(ie. `0xff` to `0x55`).  Simply modulating voltages during normal
operation will not acheive this. If some means is found to erase a
whole page (64 bytes), you'd find the pairing secret is right
beside this byte, so it would be erased as well. Correct operation
of the system requires the right 32 bytes in that area as well.


## Hackers Welcome

Since any _real hacker_ will discover the following in a few minutes,
we can share this information:

- the i2c bus between the main micro and the ATECC508a comes out to the rear test pads.
- anyone with a i2c bus monitor and the public-domain ATSHA204A datasheet could follow along.
- someone with a little patience could send their own commands to the security chip,
    and read the (public) data slots and configuration values.
- so everything we claim in this document could be proven, if one was properly motivated.

