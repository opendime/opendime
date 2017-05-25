
## Version 2.1 Opendime Sample

The files here are an example of what a V2.1 Opendime's filesystem
looks like, at each stage of it's lifecycle.

Specifically, these files were copied from a sample unit running
version 2.1.0 of the firmware:

```
2.1.0 time=20170524.144702 git=v2@0654716
```

With SHA256 checksum:

```
134b3b9bce30401116c511867754f2e8695077d9efeca42134f7b47aeb99e8a8
```

## Differences between V2.0 and V2.1

There are only very minor changes between the firmware
in version 2.0 versus 2.1:

- `support/style.css` is now minimized
- version number added to `variables.json` (key: `vn`)
- hover over copyright notice in HTML to see version number
- version number available over EP0 requests
- now possible to read `chain.crt` over EP0
- some changes to production selftest code


## Example `trustme.py` Output

```
Opendime USB at: /Volumes/OPENDIME

 Wallet address: 1KcJazDdetcENpjsouWSNj2QQpsryAYERk


Opendime Version: 2.1.0

      time: 20170524.144702
       git: v2@0654716
    serial: SPX6ESSUJVGVCIBAEBDTMDAK74+1155ccbebab2

Additional low-level checks:
  - correct virtual disk geometry
  - read-back over USB EP0 correct
  - good bitcoin message signing #1: 7d83db2fd520
  - good bitcoin message signing #2: dd2a1a4361f4
  - good bitcoin message signing #3: 4b91511674bf
  - good bitcoin message signing #4: d0d5e4a59891
  - good bitcoin message signing #5: 7c88662f1e1e
  - genuine per-unit factory certificate verified
  - good anti-counterfeiting test #1: 713ef118c71b
  - good anti-counterfeiting test #2: 96836726ccf2
  - good anti-counterfeiting test #3: 1f9b36c9dd9d
  - good anti-counterfeiting test #4: e3cac4a8bae0
  - good anti-counterfeiting test #5: ee57c87f4848

Looks good!

1KcJazDdetcENpjsouWSNj2QQpsryAYERk
```


## Example `rngverify.py` Output

The entropy used to pick the key was recorded in `entropy.bin`
and can be verified using `unsealed/advanced/rngverify.py`.

```
% ./advanced/rngverify.py .../v2.1/entropy.bin 

STEP1: Secret exponent is hash of things we expected (good).

SUCCESS: Private key uses secret exponent we expected. Perfect.

```
