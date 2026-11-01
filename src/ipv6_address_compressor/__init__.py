"""Compress expanded IPv6 addresses to RFC 5952 canonical short form."""

from .core import compress, is_valid, expand

__all__ = ["compress", "is_valid", "expand"]
