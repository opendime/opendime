
## Version 2 Opendime

In the new version of the hardware (now with layard hole) we've added another
chip which support some anti-counterfieting features.

To understand how that works, you should read the
[technical white paper here](opendime-trust-features.md)

The other files here are an example of what a V2 Opendime's filesystem looks like.


## PRE-RELEASE / Draft

Both the white paper and these images are not yet final, however, we consider
this verison to be the "release candidate".

```
2.0.0 time=20170227.113404 git=v2@a44f83a
```

                                        

## Example `trustme.py` Output

```
[sealed/advanced] % ./trustme.py /Volumes/OPENDIME
Downloading pycoin (wait)...

Opendime USB at: /Volumes/OPENDIME

 Wallet address: 1E7WUNVtXRLt15tG1JnAPue4YGgVC5oPHA


Opendime Version: 2.0.0

      time: 20170227.113404
       git: v2@a44f83a
    serial: 5NXBX5CUJVGVCIBAEBDTSGYK74+b134e591d2ba

Additional low-level checks:
  - correct virtual disk geometry
  - read-back over USB EP0 correct
  - good bitcoin message signing #1: 0d6e6a450f78
  - good bitcoin message signing #2: 2ffb105d2dc8
  - good bitcoin message signing #3: 0ff201d09e4b
  - good bitcoin message signing #4: edc9a55c0572
  - good bitcoin message signing #5: 2bf5a43eb25f
  - genuine per-unit factory certificate verified
  - good anti-counterfeiting test #1: b1bbc2265d5d
  - good anti-counterfeiting test #2: 06305607a781
  - good anti-counterfeiting test #3: 876900cdb225
  - good anti-counterfeiting test #4: 6a21f41e453f
  - good anti-counterfeiting test #5: 3981e8a49a88

Looks good!

1E7WUNVtXRLt15tG1JnAPue4YGgVC5oPHA
```
