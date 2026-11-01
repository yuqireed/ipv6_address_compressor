# ipv6_address_compressor

Compress expanded IPv6 addresses to RFC 5952 canonical short form.

## Usage

```python
from ipv6_address_compressor import compress, expand, is_valid

compress("2001:0db8:85a3:0000:0000:8a2e:0370:7334")
# '2001:db8:85a3::8a2e:370:7334'

expand("::1")
# '0000:0000:0000:0000:0000:0000:0000:0001'

is_valid("2001:db8::1")
# True
```

## Why this exists

IPv6 addresses have a single canonical textual form, but real-world data is
messy: logs uppercase the hex, configuration files carry the fully expanded
form, and embedded IPv4 tails (`::ffff:192.0.2.1`) show up wherever IPv4 and
IPv6 worlds meet. Comparing two strings for equality is therefore unreliable
unless both sides have been normalized first.

The standard library's `ipaddress.IPv6Address` already does the heavy lifting,
so this library is a thin, dependency-free wrapper that fixes the *policy*:
the output is always the RFC 5952 canonical form, and the parser accepts any
form the stdlib accepts. The trade-off is that we do not offer a streaming or
zero-allocation API; the entire address is parsed into an `IPv6Address` object
before being rendered. For address-sized inputs that cost is irrelevant, and
it keeps the code small enough to audit in one sitting.

The awkward edge you will hit: RFC 5952 says only runs of *two or more* zero
groups may be replaced by `::`, and when two runs tie in length the leftmost
one wins. A single zero group is never compressed. `compress("2001:db8:0:1:1:1:1:1")`
returns the address unchanged, which surprises people who expect every zero to
disappear.

## API

- `compress(address: str) -> str` — RFC 5952 canonical short form. Raises
  `ValueError` on malformed input and `TypeError` on non-string input.
- `expand(address: str) -> str` — fully expanded, zero-padded form.
- `is_valid(address) -> bool` — `True` for valid IPv6 text, `False` otherwise
  (including for non-string input).

## Tests

```
PYTHONPATH=src python -m unittest discover -s tests
```
