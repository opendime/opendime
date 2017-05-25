# Variables.json

See: `advanced/variables.json`

This file exists as a convenience. It contains all the values needed
to interact with the Opendime in a single file. Depending on the
state of the device, some values will be missing or blank. It is a standard
JSON file, with two-letter keys.

Variable length fields, such as the bitcoin address (`ad`) and
private key (`pk`) may be padded with spaces.

## Fields


Key | Value
---|------------
ad | Bitcoin address in base58. Same as `address.txt`
pk | Private key in WIF format (base58). Same as `private-key.txt`
sn | Serial number for main micro (base16)
ae | Serial number for ATECC508A chip (hex, lower case)
ex | Secret exponent; equivilent to pk value
on | Opendime nonce: see `advanced/rngverify.py` for background
va | Bitcoin signature over a nonce, same as `sealed/advanced/verify2.txt`
vn | Version number (only on `2.1.0` and later)


# Examples

## Factory Fresh

```javascript
{
"sn": "4QR6SUSUJVGVCIBAEBDTIHQK74",
"ae": "c5adbafe8b3d",
"vn": "2.1.0"  
}
```

## Sealed

```javascript
{
"ad": "1E8t4b3bSoVPGPW84D2i8pJs3ckK6fuRaH   ",
"pk": "SEALED                                             ",
"ex": "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
"on": "0000000000000000000000000000000000000000000000000000000000000000",
"sn": "4QR6SUSUJVGVCIBAEBDTIHQK74",
"ae": "c5adbafe8b3d",
"va": "nonce:de4d7305d43ff42121f0c4f7|1E8t4b3bSoVPGPW84D2i8pJs3ckK6fuRaH|Gzuis4coo2yxlN9QXBwb-rJzcJNitJUyBvIGexUP95yw-url5YObNITjP6320pGJVB0UBboDjBNWLqsfWuMvFXY|S"           
}
```


## Unsealed

```javascript
{
"ad": "1E8t4b3bSoVPGPW84D2i8pJs3ckK6fuRaH   ",
"pk": "5KZ13kVzh9G8m7B6cS8QxQQ6E37wRwTgHAcoKEAPRe7vs1rxuXH",
"ex": "e4af8379ce016e415c2fe6d2962958c7fafa95c13bced23ee9356a5cf1c7c156",
"on": "6778b1e7e0f28c1fd38d0c488b06ad230c8846a10f8471e5da30e431b48d10b0",
"sn": "4QR6SUSUJVGVCIBAEBDTIHQK74",
"ae": "c5adbafe8b3d",
"va": "nonce:de4d7305d43ff42121f0c4f7|1E8t4b3bSoVPGPW84D2i8pJs3ckK6fuRaH|Gzuis4coo2yxlN9QXBwb-rJzcJNitJUyBvIGexUP95yw-url5YObNITjP6320pGJVB0UBboDjBNWLqsfWuMvFXY|U"           
}
```


# History

Version 1 devices did not have fields `ae` and `sn`, and when factory fresh, did not
have any `variables.json` file at all.

