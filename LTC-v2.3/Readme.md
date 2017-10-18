# Litecoin Version

## Version 2.3 (LITECOIN) Opendime Sample

The files here are an example of what a V2.3 Opendime's filesystem
looks like, at each stage of it's lifecycle.

Specifically, these files were copied from a sample unit running
version 2.3.0 (for LITECOIN) of the firmware:

```
2.3.0 time=20171018.143523 git=master@8fb7cfd coin=LTC
```

With SHA256 checksum:

```
b296da903ee0366623effcbb1acc9db0832af2608dd43e500a1580f2ac270d13
```

## Differences between V2.3 and V2.2

There are many differences, but mainly this version is specifically for Litecoin.

- New 'ct' value in `variables.json` with BTC or LTC value
- New EP0 request to ask for coin type (either BTC or LTC)
- Version string now has "coin=LTC" value, as appropriate
- New batch certificate (#3) because it's time.


## Example `trustme.py` Output

```
Opendime USB at: /Volumes/OPENDIME

 Wallet address: Laj1Gfg7VeZgxmzSNqS7evdPUhrkR4kSAt


Opendime Version: 2.3.0

      time: 20171018.143523
       git: master@8fb7cfd
      coin: LTC
    serial: ESMLHKKSLFFVASRRFYYD6KYE74+739df4df98e3

Additional low-level checks:
  - correct virtual disk geometry
  - read-back over USB EP0 correct
  - good bitcoin message signing #1: 72764b10115a
  - good bitcoin message signing #2: 15703dfcdb85
  - good bitcoin message signing #3: c7e7a35bc241
  - good bitcoin message signing #4: 2601729cd8b5
  - good bitcoin message signing #5: d783e35d48ee
  - genuine per-unit factory certificate verified
  - good anti-counterfeiting test #1: 3b8002085068
  - good anti-counterfeiting test #2: 873656f1611b
  - good anti-counterfeiting test #3: 2afb062291f6
  - good anti-counterfeiting test #4: 0fad163fc933
  - good anti-counterfeiting test #5: 2cb0ef631ff7

Looks good!

Laj1Gfg7VeZgxmzSNqS7evdPUhrkR4kSAt
```


## Example `rngverify.py` Output

The entropy used to pick the key was recorded in `entropy.bin`
and can be verified using `unsealed/advanced/rngverify.py`.

```
% ./advanced/rngverify.py ../entropy.bin 

STEP1: Secret exponent is hash of things we expected (good).

SUCCESS: Private key uses secret exponent we expected. Perfect.
```
