# OPENDIME

Opendime is a small USB stick that allows you to spend Bitcoin like a dollar bill.
Pass 'em around!

## What's here?

This is a copy of contents of an example Opendime unit running the latest version
of the firmware. You can use this to look at how it works, and to read the 
opensource code we provide.

There are three states for an Opendime:

1) **New unit** (does not have a bitcoin address yet)
2) **Sealed** (normal; has a payment address)
2) **Un-Sealed** (private key is revealed; sweep your funds)


## How to view?

Clone this repo and then `cd new`. That's exactly what you would
see on the Opendime when you first plug it in. On MacOS, this would
be exactly the contents of `/Volumes/OPENDIME`.

In this example, we copied `entropy.bin` onto the drive to help it pick a random
private key. Once that's done, the disk drive will look like `sealed` and that's
how you'd use the Opendime most of the time.

Finally, look at `unsealed` to see what it looks like when you break the tab on
the Opendime. The private key is revealed, and in combination with the original
entropy file, you can verify we picked the private key in the manner we asserted.


## Checking the private key math

To prove we are using the algorithm we claim, perform these steps:

```bash
pip install pycoin
cd unsealed/advanced
python rngverify.py ../../entropy.bin
```


Of course, you should also contemplate the python
code in [`rngverify.py`](blob/master/unsealed/advanced/rngverify.py)
... but it's pretty simple and only 75 lines.


## What else is there to see?

You can unzip the `support/pycode.py` code to see the simple balance
check and spending code.
