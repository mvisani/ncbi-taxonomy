"""Example script to build a NCBI Taxonomy version."""

import argparse

from tqdm.auto import tqdm

from ncbi_taxonomy import Dataset, DatasetSettings


def build_ncbi_taxonomy(version: str) -> Dataset:
    """Build a version of the NCBI Taxonomy."""
    settings = DatasetSettings(version=version).include_all().set_verbose()
    return Dataset.build(settings)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Build a version of the NCBI Taxonomy."
    )
    parser.add_argument(
        "version",
        type=str,
        help="The version of the NCBI Taxonomy to build.",
    )

    args = parser.parse_args()

    if args.version == "all":
        versions = DatasetSettings.available_versions()
    else:
        versions = [args.version]

    for v in tqdm(
        versions,
        desc="Building NCBI Taxonomy",
        unit="version",
        disable=len(versions) == 1,
    ):
        _dataset: Dataset = build_ncbi_taxonomy(v)
