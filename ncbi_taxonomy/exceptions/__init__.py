"""Submodule defining exceptions used across the NCBI taxonomy."""

from ncbi_taxonomy.exceptions.unavailable_entry import UnavailableEntry
from ncbi_taxonomy.exceptions.version_exception import VersionException

__all__ = [
    "UnavailableEntry",
    "VersionException",
]
