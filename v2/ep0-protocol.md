
# Low-Level USB Protocol Details

Here we document the vendor-specific control transfers
we support for EP0.

## Background

- nearly everything is binary here
- you must provide the correct size buffers, in general
- to write, do an OUT:
  `bmRequestType=0x40`, `bRequest=0`, `wValue=command_code`,
  data is empty or binary block. Command codes are ascii letters
  by convention
- to read, do an IN: `bmRequestType=0xc0`, `bRequest=0`, `wValue=command_code`,
  data should be big enough, perhaps 2k max. Command codes are binary values
  starting at one.
- command which are inappropriate for current state of device will fail

## "IN" Transfers (get value)

CODE | Description
-----|------------
1 | Secret exponent (if unsealed)
2 | WIF version of private key (if unsealed)
3 | Bitcoin payment address (if set yet)
4 | Result of previous signature request (`m` or `f`), 65 or 96 bytes
5 | Firmware checksum (32 bytes)
6 | Firmware version as a string
7 | Readback unit x.509 certificate `unit.crt`
8 | Serial number of ATECC508A chip (6 bytes)
9 | Readback number of bytes entropy so far (unsigned LE32)

## "OUT" Transfers (set value)

CODE | Expects | Description
-----|---------|------------
`m`  | 32 bytes| Starts the bitcoin message-signing process (get result with 4)
`f`  | 20 bytes| Starts signature process in ATECC508A (get result with 4)
`E`  | n/a     | Simulate a USB hotplug to reset port
`e`  | 32 or 0 | Add 32 bytes of entropy, or reset process with 0 length transfer
`s`  | none    | Perform self-test, indicate result on LED's (unit must not have bitcoin key)
`r`  | none    | Make LED go solid red.
`o`  | none    | Restore normal LED operation.


