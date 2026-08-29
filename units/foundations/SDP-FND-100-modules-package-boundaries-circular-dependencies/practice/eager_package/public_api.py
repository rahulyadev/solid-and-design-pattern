"""A re-exported module loaded eagerly by the package initializer."""

from . import TRACE

TRACE.append("public-api")
PUBLIC_VALUE = "public-value"
