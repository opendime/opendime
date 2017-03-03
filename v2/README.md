
## Version 2 Opendime

In the new version of the hardware (now with layard hole), we've added another
chip which support some anti-counterfeiting features.

To understand how that works, you should read the
[technical white paper here](opendime-trust-features.md)

The other files here are an example of what a V2 Opendime's filesystem
looks like, at each stage of it's lifecycle.

Specifically, these files were copied from a sample unit running
version 2.0.0 of the firmware:

```
2.0.0 time=20170302.104741 git=v2@029526e
```

With SHA256 checksum:

```
04ea97186f9b61a5b8bf22188d58aac6866454dc8ebb6501a29f604d9aa8cf8e
```


## Example `trustme.py` Output

```
[sealed/advanced] % ./trustme.py /Volumes/OPENDIME
Downloading pycoin (wait)...

Opendime USB at: /Volumes/OPENDIME

 Wallet address: 1E8t4b3bSoVPGPW84D2i8pJs3ckK6fuRaH


Opendime Version: 2.0.0

      time: 20170302.104741
       git: v2@029526e
    serial: 4QR6SUSUJVGVCIBAEBDTIHQK74+c5adbafe8b3d

Additional low-level checks:
  - correct virtual disk geometry
  - read-back over USB EP0 correct
  - good bitcoin message signing #1: 7046e4111e01
  - good bitcoin message signing #2: 232339010525
  - good bitcoin message signing #3: 3b3108f30eb2
  - good bitcoin message signing #4: 865650a40f63
  - good bitcoin message signing #5: 4ee9f87c6c07
  - genuine per-unit factory certificate verified
  - good anti-counterfeiting test #1: dea6578c99ca
  - good anti-counterfeiting test #2: 98b1311f04ae
  - good anti-counterfeiting test #3: 298a2377af1b
  - good anti-counterfeiting test #4: dd05d858f858
  - good anti-counterfeiting test #5: ede300dff9fb

Looks good!

1E8t4b3bSoVPGPW84D2i8pJs3ckK6fuRaH
```
