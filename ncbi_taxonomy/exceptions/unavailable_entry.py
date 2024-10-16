"""Submodule providing the UnavailableEntry exception for the NCBI Taxonomy."""


class UnavailableEntry(ValueError):
    """Exception raised when an entry is not available."""

    def __init__(self, entry_name: str, available_entries: list[str]):
        """Initialize the unavailable entry exception."""
        super().__init__(
            f"Entry {entry_name} not found in available entries: {available_entries}"
        )
