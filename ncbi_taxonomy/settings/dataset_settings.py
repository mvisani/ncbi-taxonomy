"""Submodule providing the settings for constructing versions of the NCBI Taxonomy dataset."""

import os
from typing import Any, Dict, List

import compress_json

from ncbi_taxonomy.exceptions import UnavailableEntry, VersionException
from ncbi_taxonomy.utils.download_objective import DownloadObjective


class DatasetSettings:
    """Class defining the settings for constructing versions of the NCBI taxonomy."""

    def __init__(self, version: str):
        """Initialize the settings for constructing versions of the NCBI taxonomy."""
        local_version_path = os.path.join(
            os.path.dirname(__file__), "versions", f"{version}.json"
        )
        if not os.path.exists(local_version_path):
            available_versions = os.listdir(
                os.path.join(os.path.dirname(__file__), "versions")
            )
            raise VersionException(version, available_versions)

        self._version_metadata: Dict[str, Any] = compress_json.load(local_version_path)
        self._verbose: bool = False
        self._to_include: List[str] = []
        self._downloads_directory: str = "downloads"

    @staticmethod
    def available_versions() -> List[str]:
        """Return a list of available versions of the NCBI Taxonomy."""
        return [
            version.replace(".json", "")
            for version in os.listdir(
                os.path.join(os.path.dirname(__file__), "versions")
            )
        ]

    def download_objectives(self) -> List[DownloadObjective]:
        """Return the download objectives."""
        download_objectives: List[DownloadObjective] = []
        for included in self._to_include:
            url = self._version_metadata[included]
            file_name = url.split("/")[-1]
            path = os.path.join(
                self._downloads_directory, self._version_metadata["version"], file_name
            )
            download_objectives.append(DownloadObjective(path, url))

        return download_objectives

    def into_dict(self) -> Dict[str, Any]:
        """Return the settings as a dictionary."""
        return {
            "version_metadata": self._version_metadata,
            "verbose": self._verbose,
            "to_include": self._to_include,
            "downloads_directory": self._downloads_directory,
        }

    def include_owl(self) -> "DatasetSettings":
        """Include the OWL data in the download objectives."""
        self._owl_data = True
        return self

    def include_json(self) -> "DatasetSettings":
        """Include the JSON data in the download objectives."""
        self._json_data = True
        return self

    def set_downloads_directory(self, directory: str) -> "DatasetSettings":
        """Sets the directory to download files."""
        self._downloads_directory = directory
        return self

    def _include(self, key: str) -> "DatasetSettings":
        """Include a specific key."""
        if key not in self._version_metadata:
            raise UnavailableEntry(
                key,
                list(
                    {
                        key
                        for key in self._version_metadata.keys()
                        if key not in ["version", "year", "month", "day"]
                    }
                ),
            )
        if key not in self._to_include:
            self._to_include.append(key)
        return self

    @property
    def verbose(self) -> bool:
        """Return whether the settings are in verbose mode."""
        return self._verbose

    def set_verbose(self) -> "DatasetSettings":
        """Sets to verbose mode."""
        self._verbose = True
        return self

    def include_tsv(self) -> "DatasetSettings":
        """Include the TSV data in the download objectives."""
        return self._include("tsv")

    def include_json(self) -> "DatasetSettings":
        """Include the JSON data in the download objectives."""
        return self._include("json")

    def include_owl(self) -> "DatasetSettings":
        """Include the OWL data in the download objectives."""
        return self._include("owl")

    def include_all(self) -> "DatasetSettings":
        """Include all keys."""
        for key in self._version_metadata.keys():
            if key not in ["version", "year", "month", "day"]:
                self._to_include.append(key)
        return self
