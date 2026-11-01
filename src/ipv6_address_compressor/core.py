"""Core IPv6 address compression logic.

This module implements the textual representation rules from RFC 5952:

* Leading zeros in each 16-bit group are removed.
* The longest run of two or more zero groups is replaced by ``::``.
  When two runs tie, the first (leftmost) one wins.
* Hex digits are lowercase.

The parser also accepts a few forms that are not RFC 5952 canonical so that
users can feed in addresses copied from logs, ``/etc/hosts``, or ``ip addr``
output: uppercase hex, embedded IPv4 tails (``::ffff:192.0.2.1``), and mixed
case. The *output* is always canonical.
"""

from __future__ import annotations

import ipaddress

__all__ = ["compress", "is_valid", "expand"]


def _parse(address: str) -> ipaddress.IPv6Address:
    """Parse an address string into an ``IPv6Address``.

    ``ipaddress`` already handles zone identifiers, embedded IPv4 tails, and
    the full RFC 4291 grammar. We only add a clearer error message and reject
    non-string inputs up front so callers get a ``TypeError`` rather than a
    confusing ``AttributeError`` from deep inside the stdlib.
    """
    if not isinstance(address, str):
        raise TypeError(
            "address must be a string, got {!r}".format(type(address).__name__)
        )
    return ipaddress.IPv6Address(address)


def compress(address: str) -> str:
    """Return the RFC 5952 canonical short form of *address*.

    The input may be any IPv6 textual form that the standard library accepts,
    including uppercase hex and an embedded IPv4 tail. The output is always
    lowercase with a single ``::`` at the leftmost longest zero run.

    Raises ``ValueError`` for malformed addresses and ``TypeError`` for
    non-string input.
    """
    return _parse(address).compressed


def expand(address: str) -> str:
    """Return the fully expanded, zero-padded form of *address*.

    This is the inverse of :func:`compress` in the sense that feeding the
    result back into :func:`compress` yields the canonical form. It is useful
    for byte-exact comparisons and for sorting addresses lexically.
    """
    return _parse(address).exploded


def is_valid(address: str) -> bool:
    """Return ``True`` if *address* is a syntactically valid IPv6 address.

    Non-string input returns ``False`` rather than raising, because callers
    frequently use this as a guard before calling :func:`compress` on data of
    unknown provenance.
    """
    try:
        _parse(address)
    except (TypeError, ValueError):
        return False
    return True
