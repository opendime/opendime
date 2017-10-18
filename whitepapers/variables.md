# Variables.json

See: `advanced/variables.json`

This file exists as a convenience. It contains all the values needed
to interact with the Opendime in a single file. Depending on the
state of the device, some values will be missing or blank. It is a standard
JSON file, with two-letter keys.

Variable length fields, such as the bitcoin address (`ad`) and
private key (`pk`) will be padded with spaces.

## Fields


Key | Value
---|------------
ad | Bitcoin address in base58. Same as `address.txt`
pk | Private key in WIF format (base58). Same as `private-key.txt`
sn | Serial number for main micro (base16)
ae | Serial number for ATECC508A chip (hex, lower case)
ex | Secret exponent; equivalent to pk value
on | Opendime nonce: see `advanced/rngverify.py` for background
va | Bitcoin signature over a nonce, same as `sealed/advanced/verify2.txt`
vn | Version number (only on `2.1.0` and later)
ct | Coin type (BTC, LTC, etc) (only on `2.3.0` and later, assume BTC otherwise)


# Examples

## Factory Fresh

```javascript
{
"sn": "SPX6ESSUJVGVCIBAEBDTMDAK74",
"ae": "1155ccbebab2",
"vn": "2.1.0"  
}
```

## Sealed

```javascript
{
"ad": "1KcJazDdetcENpjsouWSNj2QQpsryAYERk   ",
"pk": "SEALED                                             ",
"ex": "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
"on": "0000000000000000000000000000000000000000000000000000000000000000",
"sn": "SPX6ESSUJVGVCIBAEBDTMDAK74",
"ae": "1155ccbebab2",
"va": "nonce:6025386306d061b37dc8dc29|1KcJazDdetcENpjsouWSNj2QQpsryAYERk|G0s2X6EaJ6Sbw2xeE8q5-NYcLqNgomliWFas6hlBVShn6XJhSfSEsLNWzNieuEmzFZrBoiToSUUho-8_KzzFwp8|S"           ,
"vn": "2.1.0"  
}
```


## Unsealed

```javascript
{
"ad": "1KcJazDdetcENpjsouWSNj2QQpsryAYERk   ",
"pk": "5KML3zBUnMsdYjwXqzzDPPSZm5tP2ToryDyxkkN8aNRnre2vL5i",
"ex": "ca2e9f22257462ce00e7cdd3c853b8bb14cec5ff776b11f4046ab7ae5de6553a",
"on": "da9559ded92b02c56428c816b1c6ba15e61ee400eaa20122f937e34097e5a117",
"sn": "SPX6ESSUJVGVCIBAEBDTMDAK74",
"ae": "1155ccbebab2",
"va": "nonce:6025386306d061b37dc8dc29|1KcJazDdetcENpjsouWSNj2QQpsryAYERk|G0s2X6EaJ6Sbw2xeE8q5-NYcLqNgomliWFas6hlBVShn6XJhSfSEsLNWzNieuEmzFZrBoiToSUUho-8_KzzFwp8|U"           ,
"vn": "2.1.0"  
}
```


# History

- Version 1 devices did not have fields `ae` and `sn`, and when factory fresh, did not
have any `variables.json` file at all.

- Version 2.0 devices did not have `vn` (version number) field.

