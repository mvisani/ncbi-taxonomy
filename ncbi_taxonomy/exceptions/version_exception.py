"""Submodule providing the version exception for the NCBI taxonomy."""


class VersionException(ValueError):
    """Exception raised when an invalid version is provided."""

    def __init__(self, version: str, available_versions: list[str]):
        """Initialize the version exception."""
        super().__init__(
            f"Version {version} not found in available versions: {available_versions}"
        )
