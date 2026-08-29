"""A leaf whose import must first execute the parent package initializer."""

from . import TRACE

TRACE.append("leaf")
LEAF_VALUE = "leaf-value"
