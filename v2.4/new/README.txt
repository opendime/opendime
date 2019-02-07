Welcome to Opendime USB
=======================

TL;DR ... Write random files here to get started.

Setup Time
----------

This Opendime is fresh and unused. It hasn't picked a private key yet.

It needs more random numbers!

All you have to do is save files onto this virtual drive. It will
add all the randomness from those files into it's own random number
generator.

It doesn't matter what the files are, and they are **not** preserved.

Photos that only you would have are great, or you could save bits
from from random.org or /dev/urandom:

<https://www.random.org/cgi-bin/randbyte?nbytes=16384&format=f>

Once you've saved at least 256k random bytes, your new payment
address will be automatically generated.

(You may see a a warning about ejecting disks before unplugging them,
but that's safe to ignore.)


MacOS X
-------

From terminal, this command line will do what's needed:

    dd if=/dev/urandom of=/Volumes/OPENDIME/entro.bin bs=1024 count=256

But it's really just as good to drop a photo of your cat onto the drive.

Unix and Linux users can also dd from /dev/urandom onto the drive,
but you would need to know where it's mounted. The file name used
(entro.bin in above example) does not matter.


Lots of Flashing Red Lights?
----------------------------

If the seal on the Opendime is broken before we pick a private key,
it will stay in this failed state, but flash the red and green
lights quickly. Next time, do not break the seal until **AFTER**
the private key has been picked, and funds loaded onto the address.


Legal Notice
------------

By purchasing, using or continuing to use the Opendime USB stick,
you, the purchaser of the Product, agree to be bound by the terms
of sale and use:

    support/terms.txt

    https://opendime.com/legal


