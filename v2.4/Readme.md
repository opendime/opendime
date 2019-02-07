
## Version 2.4 Opendime Sample

The files here are an example of what a V2.4.0 Opendime's filesystem
looks like, at each stage of it's lifecycle.

Specifically, these files were copied from a sample unit running
version 2.4.0 of the firmware:

```
2.4.0 time=20190207.130255 git=master@e233940e coin=BTC
                          
```

With SHA256 checksum:

```
757a9feed49a2d5463081703a66a604509e41392d97d6b16554ed6e07cddfe81
```

## New Changes in this Version

- if the user's browser is set for language we have a translation for, we'll show that instead of English (can still override)
- blockchain explorers updated: Blocktrail removed, BC.i becomes BC.com, add Blockstream
- copyright changed to 2016-2019. added (R) to Opendime logo (we are registered now)
- changes to match v4 hardware
- `version.txt` now includes `coin=BTC` as a value
- `chain.crt` has certificate chain for "Batch #4" from the factory


## Example `trustme.py` Output

```
Opendime USB at: /Volumes/OPENDIME

 Wallet address: 1P431tezawsLq7ZDPqfp8CnGGKxuYpLTKR


Opendime Version: 2.4.0

      time: 20190207.130255
       git: master@e233940e
      coin: BTC
    serial: JETJEECBIZIFCIBAEBGDGBIU74+de5cc35e8548

Additional low-level checks:
  - correct virtual disk geometry
  - read-back over USB EP0 correct
  - good bitcoin message signing #1: d58cf51fb25e
  - good bitcoin message signing #2: 691f49d92a69
  - good bitcoin message signing #3: e52f813f5ad4
  - good bitcoin message signing #4: 96f5a328bf51
  - good bitcoin message signing #5: 9c4898dd64c1
  - genuine per-unit factory certificate verified
  - good anti-counterfeiting test #1: 810082168642
  - good anti-counterfeiting test #2: ae686c33628f
  - good anti-counterfeiting test #3: ce632878c71b
  - good anti-counterfeiting test #4: 934a008b55ec
  - good anti-counterfeiting test #5: 4c14200b1aec

Looks good!

1P431tezawsLq7ZDPqfp8CnGGKxuYpLTKR
```


## Example `rngverify.py` Output

The entropy used to pick the key was recorded in `entropy.bin`
and can be verified using `unsealed/advanced/rngverify.py`.

```
% ./advanced/rngverify.py entropy.bin 

STEP1: Secret exponent is hash of things we expected (good).

SUCCESS: Private key uses secret exponent we expected. Perfect.

```
