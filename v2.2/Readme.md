
## Version 2.2 Opendime Sample

The files here are an example of what a V2.2 Opendime's filesystem
looks like, at each stage of it's lifecycle.

Specifically, these files were copied from a sample unit running
version 2.2.0 of the firmware:

```
2.2.0 time=20170721.115213 git=v3@d0c4b54
```

With SHA256 checksum:

```
753ec10262f92c6bbe4f9a01e440278c36c2c8352ed897a75aabb0993d63ab9a
```

## Differences between V2.1 and V2.2

There are only very minor changes between the firmware
in version 2.1 versus 2.2:

- Improved Japanese translation text
- New batch certificate (#2) for first build of version 3.0 hardware


## Example `trustme.py` Output

```
Opendime USB at: /Volumes/OPENDIME

 Wallet address: 1PCejtxqj92B5bn3nqP6dp1jjybS3iGD6a


Opendime Version: 2.2.0

      time: 20170721.115213
       git: v3@d0c4b54
    serial: SPX6ESSUJVGVCIBAEBDTMDAK74+0855ccbebab2

Additional low-level checks:
  - correct virtual disk geometry
  - read-back over USB EP0 correct
  - good bitcoin message signing #1: fba39eeffa0d
  - good bitcoin message signing #2: d7b7302e48bb
  - good bitcoin message signing #3: b88b13038ce3
  - good bitcoin message signing #4: 82cefe91ea37
  - good bitcoin message signing #5: c3b06f6905b7
  - genuine per-unit factory certificate verified
  - good anti-counterfeiting test #1: 3b766a52a6f7
  - good anti-counterfeiting test #2: b4545744d08f
  - good anti-counterfeiting test #3: 3a405baeabad
  - good anti-counterfeiting test #4: 9593f40b0bc9
  - good anti-counterfeiting test #5: 683a246f2122

Looks good!

1PCejtxqj92B5bn3nqP6dp1jjybS3iGD6a
```


## Example `rngverify.py` Output

The entropy used to pick the key was recorded in `entropy.bin`
and can be verified using `unsealed/advanced/rngverify.py`.

```
% ./advanced/rngverify.py .../v2.2/entropy.bin 

STEP1: Secret exponent is hash of things we expected (good).

SUCCESS: Private key uses secret exponent we expected. Perfect.

```
