from typing import Any, Dict, List, Set

from downloaders import BaseDownloader
from tqdm.auto import tqdm

from ncbi_taxonomy.settings.dataset_settings import DatasetSettings


class Dataset:
    """Class representing a the NCBI taxonomy dataset."""

    def __init__(self, metadata: Dict[str, Any]):
        """Initialize the NCBI Taxonomy Dataset."""

    @staticmethod
    def build(settings: DatasetSettings) -> "Dataset":
        """Build a dataset from the settings."""
        paths: List[str] = []
        urls: List[str] = []

        for objective in settings.download_objectives():
            paths.append(objective.path)
            urls.append(objective.url)

        BaseDownloader(
            process_number=1,
            verbose=settings.verbose,
            # sleep_time=2,
        ).download(urls=urls, paths=paths)

        return Dataset(metadata=settings.into_dict())
