Welcome to Opendime USB
=======================

TL;DR ... Open "index.htm" to get started.


How do I know this is a legit Opendime?
---------------------------------------

- check that "verify.txt" and "verify2.txt" change each time you plug in
- check the light flashes like described below
- see the files in "advanced" subdirectory, and run "python trustme.py"
- verify the message signature in "verify2.txt" using any Bitcoin wallet or website
- visit any of the major block explorers and check balance
- see "index.htm" for more links and FAQ


How do I get my funds out?
--------------------------

To be able to move these funds, you must BREAK out the cover over the hole
in the Opendime. Look for the circle and arrow on back side.

Once that piece has been broken out, the file contents here will
change and the private key will be revealed in the private-key.txt file
and QR code image. There is no way back, and once unsealed, you
should move the funds into another wallet.

Import the private key (private-key.txt) into any Bitcoin wallet
to be able to "sweep up" the funds and spend them as needed.

There is also a python program (advanced/balance.py) which can be
used to move the funds out and check balance when sealed.


What the Light Means
--------------------

There is one red and one green light on the Opendime. The lights
will work correctly even without a computer; just connect the
Opendime to a USB charger or power pack.

Lights will flash as follows:

- Green with brief flicker:
    Sealed. Your funds are secure.

- Red and green alternating: 
    UNSEALED. Private key has been revealed.

- Green solid, brief flash of red:
    Not yet loaded with enough entropy (setup time).

- Green flashing (fast):
    Reading/writing to drive.

These specific patterns have been chosen so that it's hard to
fake the flashing pattern with small hardware changes.


File Listing
------------

index.htm       - helpful HTML file; double click this to view
address.txt     - payment address for deposit (just that, nothing more)
private-key.txt - private key for import (sweep) into a wallet (WIF format)
qrcode.jpg      - QR image of the payment address or private key
README.txt      - this file that you are reading right now

advanced/       - (directory) more technical data and files...
  checksum.txt    - SHA256 of the firmware being used on this Opendime
  verify.txt      - longer signed message, for verification of private key
  verify2.txt     - shorter signed message, which is easier to cut-n-paste into other tools
  balance.py      - python program that can display current balance and remove funds
  trustme.py      - python program which verifies authenticity of this unit, or another
  rngverify.py    - python program used to verify we are honestly generating the private key
  variables.json  - JSON file of the address and other values for this opendime
  version.txt     - date/time and version number of the firmware
  checksum.txt    - SHA256 checksum of the firmware
  chain.crt       - X.509 certificate chain back to Opendime factory CA
  unit.crt        - X.509 certificate for this particular Opendime

support/        - (directory) supporting files that aren't interesting
DCIM/           - (directory) hidden directory to support iPad usage (ignore)

The 'private-key.txt' file will be useless until the device is
"unsealed".  At the same time, the contents of 'index.html' and
'qrcode.png' will change to reveal the private key when unsealed.
Other files are not affected by unsealing.

Everything is read-only! You can't change any files on this drive.


Legal Notice
------------

By purchasing, using or continuing to use the Opendime USB stick,
you, the purchaser of the Product, agree to be bound by the terms
of sale and use:

    support/terms.txt

    https://opendime.com/legal


