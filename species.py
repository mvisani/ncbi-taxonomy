"""Submodule to fetch in different ways the species."""

from io import StringIO
from typing import Dict

import pandas as pd
from cache_decorator import Cache
from downloaders import BaseDownloader
from requests import request

QLEVER_URL = "https://qlever.cs.uni-freiburg.de/api/wikidata"


@Cache(
    validity_duration="8w",
    use_approximated_hash=True,
)
def sparql_to_text(query: str, url: str = QLEVER_URL, as_post: bool = False) -> str:
    """Function that sends a SPARQL query to the QLever API and returns the result as a string. The string
    is a CSV file."""
    method = "POST" if as_post else "GET"
    return request(
        method,
        url,
        params={"query": query},
        headers={
            "Accept": "text/csv",
            "Accept-Encoding": "gzip,deflate",
            "User-Agent": "LOTUS project database dumper",
        },
        timeout=70,
    ).text


@Cache(
    "{cache_dir}/{function_name}/{_hash}.csv.gz",
    use_approximated_hash=True,
)
def text_to_csv(text_from_query: str) -> pd.DataFrame:
    """Function that converts a text from a SPARQL query to a DataFrame."""
    df = pd.read_csv(StringIO(text_from_query))
    return df


def get_wikidata_taxonomy_from_root(
    wikidata: str,
    with_subspecies: bool = False,
) -> Dict[str, str]:
    """Function that returns the taxonomy starting from defined root.
    If `with_subspecies` is True, it will include subspecies. Otherwise
    it will only get all the way to the species."""
    if with_subspecies:
        query = f"""
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX wd: <http://www.wikidata.org/entity/>

        SELECT ?taxon ?taxon_name ?taxon_rank ?taxon_rank_label ?taxon_parent ?parent_name WHERE {{
          ?taxon wdt:P225 ?taxon_name;
                 wdt:P105 ?taxon_rank;
                 wdt:P171* wd:{wikidata};      # Recursively fetches all taxa with Mammal as an ancestor
                 wdt:P171 ?taxon_parent.

          ?taxon_rank rdfs:label ?taxon_rank_label.
          FILTER (lang(?taxon_rank_label) = "en")

          ?taxon_parent wdt:P225 ?parent_name.
        }}
    """
    else:
        query = f"""
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX wd: <http://www.wikidata.org/entity/>
        SELECT ?taxon ?taxon_name ?taxon_rank ?taxon_rank_label ?taxon_parent ?parent_name WHERE {{
          ?taxon wdt:P225 ?taxon_name ;
                 wdt:P105 ?taxon_rank ;
                 wdt:P171* wd:{wikidata} ;
                 # Recursively fetches all taxa with Mammal as an ancestor
          wdt:P171 ?taxon_parent .
          ?taxon_rank rdfs:label ?taxon_rank_label .
          FILTER (LANG(?taxon_rank_label) = "en")
          FILTER (?taxon_rank != wd:Q68947)
          # Exclude taxa with rank "subspecies"
          ?taxon_parent wdt:P225 ?parent_name .
        }}
        """

        # run the query
        query_output = sparql_to_text(query)

        # convert the output to a DataFrame
        taxon_to_direct_parent_only = text_to_csv(query_output)
        del query_output

        # we remove the not necessary columns : taxon_name, taxon_rank, taxon_rank_label,
        # parent_name
        taxon_to_direct_parent_only = taxon_to_direct_parent_only.drop(
            [
                "taxon_name",
                "taxon_rank",
                "taxon_rank_label",
                "parent_name",
            ],
        )

        # we convert the dataframe to a dictionary with structure (taxon: parent)
        taxon_to_direct_parent_only = taxon_to_direct_parent_only.to_dict()
        taxon_to_direct_parent_only = {
            taxon: parent
            for taxon, parent in zip(
                taxon_to_direct_parent_only["taxon"],
                taxon_to_direct_parent_only["taxon_parent"],
            )
        }

        return taxon_to_direct_parent_only


def get_lotus_from_query() -> pd.DataFrame:
    """Function that returns a dataframe with molecules and the species
    it is found in. With the paper that links them."""
    query = """
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX p: <http://www.wikidata.org/prop/>
    PREFIX ps: <http://www.wikidata.org/prop/statement/>
    PREFIX pr: <http://www.wikidata.org/prop/reference/>
    PREFIX prov: <http://www.w3.org/ns/prov#>
    SELECT DISTINCT ?structure ?structure_inchikey ?taxon ?taxon_name ?reference ?reference_doi WHERE {
      ?structure wdt:P235 ?structure_inchikey ;
                 # get the inchikey
      p:P703 ?taxon_statement .
      # find the statement node
      ?taxon_statement ps:P703 ?taxon .
      # get the taxon from the statement node
      ?taxon_statement prov:wasDerivedFrom ?ref_node .
      # get the reference node from the statement node
      ?ref_node pr:P248 ?reference .
      # get the reference item
      ?taxon wdt:P225 ?taxon_name .
      # get the taxon scientific name
      ?reference wdt:P356 ?reference_doi .
      # get the reference DOI
    }"""
    query_output = sparql_to_text(query)
    return text_to_csv(query_output)


def download_lotus_frozen_with_metadata() -> pd.DataFrame:
    """Fetches the LOTUS dataset with metadata from Zenodo."""
    url = ""
    path = ""
    return 0


def download_ncbi_taxonomy():
    return 0


# def get_lotus_taxonomy_from_root(
# wikidata: str,
# with_subspecies: bool = False,
# ) -> Dict[str, str]:
