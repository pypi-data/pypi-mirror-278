# Munud

Building payloads with sub-byte unaligned values, and generating according C code.

# Installation

The easiest way to install this library is using pip:

```bash
pip install munud
```

# Motivation

This module is built around the concept of "Unaligned Bytes", which means a sequence
of n bits forming an int which might not be aligned on the bytes themselves.

Take as an example the following bytes : 

```py
some_bytes = b"\xfa\x04\xde"
```

We will assume that the first 3 bits corresponds to value A, the next 17 bits to value B, and
the next 4 bits to value C. This will correspond to the following representation in memory:

```txt
 +--------+--------+--------+
 | Byte 0 | Byte 1 | Byte 2 |
 +---+----+--------+---+----+
 | A |        B        | C  |
 +---+-----------------+----+

```

Thus, a traditionnal python way of retrieving those three values would be as such:

```python
A = some_bytes[0] >> 5
B = (some_bytes[0] & 0x1F) << 12 | some_bytes[1] << 4 | some_bytes[2] >> 4
C = some_bytes[2] & 0x0F
```

And a traditional way of shoving those values in a byte array would be as follows:

```python
some_bytes = [0, 0, 0]

some_bytes[0] |= A << 5

some_bytes[0] |= (B >> 12) & 0x1F
some_bytes[1] = (B >> 4) & 0xFF
some_bytes[2] |= (B << 4) & 0xFF

some_bytes[2] |= C
```

This module provides two main functionalities:

- Provide a python API to do those read/write operations dynamically
- Generate a C code to perform those operations efficiently, given a fixed format

# Usage

## Programmation API

With munud, the same can be achieved using the following:

```python

from munud import UnalignedBytes

ub_A = UnalignedBytes(offset=0, bit_size=3)
ub_B = UnalignedBytes(3, 17)
ub_C = UnalignedBytes(20, 4)

# Writing
some_bytes = [0, 0, 0]

ub_A.shove(byte_buffer=some_bytes, value=3)
ub_B.shove(some_bytes, 1234)
ub_C.shove(some_bytes, 5)

# > b"\x60\x4d\x25"

# Reading
A = ub_A.extract(some_bytes)
B = ub_B.extract(some_bytes)
C = ub_C.extract(some_bytes)

```

### Using a yaml file : 

Using the following `test.yml` file:

```yml
- name: A
  size: 3
  type: uint8_t
- name: B
  size: 17
  type: uint16_t
- name: C
  size: 4
  type: uint8_t
```

Use the following to obtain a python dict representing the extracted bytes :


```python
bytes_to_read = b"\x60\x4d\x25"

from_yaml("test.yml", bytes_to_read)
# > {'A': 3, 'B': 1234, 'C': 5}

```

## C generation with the cli

Using the following `test.yml` file:

```yml
- name: A
  size: 3
  type: uint8_t
- name: B
  size: 17
  type: uint16_t
- name: C
  size: 4
  type: uint8_t
```

To show a table summarizing the payload, use :

```bash
munud -f test.yml show
```

```txt
                    Payload
┏━━━━━━━━━━┳━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃     Type ┃ Name ┃ Size (bits) ┃    Byte Span ┃
┡━━━━━━━━━━╇━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│  uint8_t │    A │ 3           │ [0 (+0) - 1] │
│ uint16_t │    B │ 17          │ [0 (+3) - 3] │
│  uint8_t │    C │ 4           │ [2 (+4) - 3] │
└──────────┴──────┴─────────────┴──────────────┘
Total payload size: 24 bits
```

To decode an hex payload, use:

```bash
munud -f test.yml decode -p AAAAAAAA
```

```
          Payload
┏━━━━━━━━━━┳━━━━━━┳━━━━━━━┓
┃     Type ┃ Name ┃ Value ┃
┡━━━━━━━━━━╇━━━━━━╇━━━━━━━┩
│  uint8_t │    A │     5 │
│ uint16_t │    B │ 43690 │
│  uint8_t │    C │    10 │
└──────────┴──────┴───────┘
Total payload size: 24 bits
```

To generate c getters and setters, use:

```bash
munud -f test.yml cgen 
```

This will generate the following c code:

```c
#include "assert.h"
#include "stdint.h"
        

inline static uint8_t get_A(uint8_t *payload)
{
    /*
     * This function retrives the value A (3 bits).
     * The value is found in byte 0.
     * The value starts at bit 0.
     */

    return payload[0] >> 5;
}

inline static void set_A(uint8_t *payload, uint8_t value)
{
    /*
     * This function writes the value A (3 bits).
     * The value will be written in byte 0.
     * The value starts at bit 0.
     */

    payload[0] |= value << 5;
}


inline static uint16_t get_B(uint8_t *payload)
{
    /*
     * This function retrives the value B (17 bits).
     * The value spreads between bytes 0 and 2.
     * The value starts at bit 3.
     */

    return (payload[0] & 0x1F) << 12 | payload[1] << 4 | payload[2] >> 4;
}

inline static void set_B(uint8_t *payload, uint16_t value)
{
    /*
     * This function writes the value B (17 bits).
     * The value will spread between bytes 0 and 2.
     * The value starts at bit 3.
     */

    payload[0] |= (value >> 12) & 0x1F;
    payload[1] = (value >> 4) & 0xFF;
    payload[2] |= (value << 4) & 0xFF;
}


inline static uint8_t get_C(uint8_t *payload)
{
    /*
     * This function retrives the value C (4 bits).
     * The value is found in byte 2.
     * The value starts at bit 4.
     */

    return payload[2] & 0x0F;
}

inline static void set_C(uint8_t *payload, uint8_t value)
{
    /*
     * This function writes the value C (4 bits).
     * The value will be written in byte 20.
     * The value starts at bit 4.
     */

    payload[2] |= value;
}


struct Payload
{

    uint16_t B;
    uint8_t A;
    uint8_t C;
};



inline static void decode(struct Payload *payload, uint8_t *packed)
{
    /*
     * 
     */

    payload->A = get_A(packed);
    payload->B = get_B(packed);
    payload->C = get_C(packed);
}

inline static void encode(struct Payload *payload, uint8_t *packed)
{
    /*
     * 
     */

    set_A(packed, payload->A);
    set_B(packed, payload->B);
    set_C(packed, payload->C);
}
```


Many options are available for customisation :

```bash

$ munud cgen --help

Usage: munud.cmd cgen [OPTIONS]

Options:
  -f, --fmt TEXT          A file describing the wanted format.
  -o, --output TEXT       The output .h file.
  --crlf                  Use \r\n (crlf) as newline instead of \n (crlf).
  --use-assert            Generate assert check before writing to payload.
  --get-only              Generate only getters.
  --set-only              Generate only setters.
  --without-struct        Do not generate a struct containing the payload.
  --packed-struct         Add the gcc __attribute__((packed)) attribute to the
                          struct.
  -n, --struct-name TEXT  Payload struct name.
  --without-safety-mask   Removes the 0xff mask when writing ints on bytes.
  --payload-type TEXT     The type of the payload, usually uint8_t*.
  --cpp                   Generate cpp-style namespace.
  --namespace TEXT        The name of an optional namespace. If cpp is not
                          enabled, add it as a prefix.
  --help                  Show this message and exit.
```

# Development

This library uses poetry as a development tool.

You can start development by running :

```bash
poetry install
```

# Testing

You can test this library using :

```bash
poetry run pytest
```

# Tox

You can test multiple python versions using tox :

```bash
poetry run tox
```
