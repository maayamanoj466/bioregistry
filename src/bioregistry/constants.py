"""Constants and utilities for registries."""

from __future__ import annotations

import enum
import os
import pathlib
import re
from typing import Union

import pystow
from curies import ReferenceTuple
from typing_extensions import TypeAlias

__all__ = [
    "BIOREGISTRY_MODULE",
    "BIOREGISTRY_PATH",
    "COLLECTIONS_PATH",
    "CURATED_MAPPINGS_PATH",
    "DATA_DIRECTORY",
    "HERE",
    "METAREGISTRY_PATH",
    "RAW_DIRECTORY",
    "FailureReturnType",
    "MaybeCURIE",
    "get_failure_return_type",
]

PATTERN_KEY = "pattern"
ORCID_PATTERN = r"^\d{4}-\d{4}-\d{4}-\d{3}(\d|X)$"

HERE = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))
DATA_DIRECTORY = HERE / "data"
EXTERNAL = DATA_DIRECTORY / "external"
BIOREGISTRY_PATH = DATA_DIRECTORY / "bioregistry.json"
METAREGISTRY_PATH = DATA_DIRECTORY / "metaregistry.json"
COLLECTIONS_PATH = DATA_DIRECTORY / "collections.json"
CURATED_MAPPINGS_PATH = DATA_DIRECTORY / "curated_mappings.sssom.tsv"
CONTEXTS_PATH = DATA_DIRECTORY / "contexts.json"
CURATED_PAPERS_PATH = DATA_DIRECTORY / "curated_papers.tsv"

BIOREGISTRY_MODULE = pystow.module("bioregistry")

ROOT = HERE.parent.parent.resolve()
DOCS = ROOT.joinpath("docs")
DOCS_DATA = DOCS.joinpath("_data")
DOCS_IMG = DOCS.joinpath("img")

EXPORT_DIRECTORY = ROOT.joinpath("exports")

METADATA_CURATION_DIRECTORY = EXPORT_DIRECTORY.joinpath("alignment")
RAW_DIRECTORY = EXPORT_DIRECTORY.joinpath("raw")
EXPORT_CONTEXTS = EXPORT_DIRECTORY / "contexts"
CONTEXT_BIOREGISTRY_PATH = EXPORT_CONTEXTS / "bioregistry.context.jsonld"
SHACL_TURTLE_PATH = EXPORT_CONTEXTS / "bioregistry.context.ttl"
CONTEXT_OBO_PATH = EXPORT_CONTEXTS / "obo.context.jsonld"
SHACL_OBO_TURTLE_PATH = EXPORT_CONTEXTS / "obo.context.ttl"
CONTEXT_OBO_SYNONYMS_PATH = EXPORT_CONTEXTS / "obo_synonyms.context.jsonld"
SHACL_OBO_SYNONYMS_TURTLE_PATH = EXPORT_CONTEXTS / "obo_synonyms.context.ttl"

EXPORT_RDF = EXPORT_DIRECTORY.joinpath("rdf")
SCHEMA_SVG_PATH = EXPORT_RDF / "schema.svg"
SCHEMA_PDF_PATH = EXPORT_RDF / "schema.pdf"
SCHEMA_TURTLE_PATH = EXPORT_RDF / "schema.ttl"
SCHEMA_NT_PATH = EXPORT_RDF / "schema.nt"
SCHEMA_JSONLD_PATH = EXPORT_RDF / "schema.jsonld"
RDF_TURTLE_PATH = EXPORT_RDF / "bioregistry.ttl"
RDF_NT_PATH = EXPORT_RDF / "bioregistry.nt"
RDF_JSONLD_PATH = EXPORT_RDF / "bioregistry.jsonld"

EXPORT_SSSOM = EXPORT_DIRECTORY.joinpath("sssom")
SSSOM_PATH = EXPORT_SSSOM / "bioregistry.sssom.tsv"
SSSOM_METADATA_PATH = EXPORT_SSSOM / "bioregistry.sssom.yml"

EXPORT_REGISTRY = EXPORT_DIRECTORY.joinpath("registry")
REGISTRY_YAML_PATH = EXPORT_REGISTRY / "registry.yml"
REGISTRY_JSON_PATH = EXPORT_REGISTRY / "registry.json"
REGISTRY_TSV_PATH = EXPORT_REGISTRY / "registry.tsv"

EXPORT_METAREGISTRY = EXPORT_DIRECTORY.joinpath("metaregistry")
METAREGISTRY_YAML_PATH = EXPORT_METAREGISTRY / "metaregistry.yml"
METAREGISTRY_TSV_PATH = EXPORT_METAREGISTRY / "metaregistry.tsv"

EXPORT_COLLECTIONS = EXPORT_DIRECTORY.joinpath("collections")
COLLECTIONS_YAML_PATH = EXPORT_COLLECTIONS / "collections.yml"
COLLECTIONS_TSV_PATH = EXPORT_COLLECTIONS / "collections.tsv"

EXPORT_TABLES = EXPORT_DIRECTORY.joinpath("tables")
TABLES_GOVERNANCE_TSV_PATH = EXPORT_TABLES.joinpath("comparison_goveranance.tsv")
TABLES_GOVERNANCE_LATEX_PATH = EXPORT_TABLES.joinpath("comparison_goveranance.tex")
TABLES_METADATA_TSV_PATH = EXPORT_TABLES.joinpath("comparison_metadata.tsv")
TABLES_METADATA_LATEX_PATH = EXPORT_TABLES.joinpath("comparison_metadata.tex")
TABLES_SUMMARY_LATEX_PATH = EXPORT_TABLES.joinpath("summary.tex")

EXPORT_ANALYSES = EXPORT_DIRECTORY.joinpath("analyses")

BENCHMARKS = EXPORT_DIRECTORY.joinpath("benchmarks")

URI_PARSING = BENCHMARKS.joinpath("uri_parsing")
URI_PARSING_DATA_PATH = URI_PARSING.joinpath("data.tsv")
URI_PARSING_SVG_PATH = URI_PARSING.joinpath("results.svg")

CURIE_PARSING = BENCHMARKS.joinpath("curie_parsing")
CURIE_PARSING_DATA_PATH = CURIE_PARSING.joinpath("data.tsv")
CURIE_PARSING_SVG_PATH = CURIE_PARSING.joinpath("results.svg")

CURIE_VALIDATION = BENCHMARKS.joinpath("curie_validation")
CURIE_VALIDATION_DATA_PATH = CURIE_VALIDATION.joinpath("data.tsv")
CURIE_VALIDATION_SVG_PATH = CURIE_VALIDATION.joinpath("results.svg")

BIOREGISTRY_DEFAULT_BASE_URL = "https://bioregistry.io"
#: The URL of the remote Bioregistry site
BIOREGISTRY_REMOTE_URL = pystow.get_config(
    "bioregistry", "url", default=BIOREGISTRY_DEFAULT_BASE_URL
)

#: Resolution is broken on identifiers.org for the following
IDOT_BROKEN = {
    "gramene.growthstage",
    "oma.hog",
    "mir",  # Added on 2021-10-08
    "storedb",  # Added on 2021-10-12
    "miriam.collection",  # Added on 2022-09-17
    "miriam.resource",  # Added on 2022-09-17
    "psipar",  # Added on 2022-09-17
}

URI_FORMAT_KEY = "uri_format"

#: MIRIAM definitions that don't make any sense
MIRIAM_BLACKLIST = {
    # this one uses the names instead of IDs, and points to a dead resource.
    # See https://github.com/identifiers-org/identifiers-org.github.io/issues/139
    "pid.pathway",
    # this uses namespace-in-namespace
    "neurolex",
    # Miriam needs to be extended
    "ccds",
    # Miriam completely misses the actual usage
    "agricola",
    # Miriam pattern/example combo is broken
    # See https://github.com/biopragmatics/bioregistry/issues/1588
    "hogenom",
    # Miriam pattern/example combo is broken
    "homd.seq",
}
IDENTIFIERS_ORG_URL_PREFIX = "https://identifiers.org/"

#: The priority list
LINK_PRIORITY = [
    "custom",
    "default",
    "bioregistry",
    "miriam",
    "ols",
    "obofoundry",
    "n2t",
    "bioportal",
    "scholia",
]
NDEX_UUID = "860647c4-f7c1-11ec-ac45-0ac135e8bacf"

SHIELDS_BASE = "https://img.shields.io/badge/dynamic"
CH_BASE = "https://cthoyt.com/obo-community-health"
HEALTH_BASE = "https://github.com/cthoyt/obo-community-health/raw/main/data/data.json"
EXTRAS = f"%20Community%20Health%20Score&link={CH_BASE}"

# not a perfect email regex, but close enough
EMAIL_RE_STR = r"^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,7}$"
EMAIL_RE = re.compile(EMAIL_RE_STR)

NonePair: TypeAlias = tuple[None, None]

MaybeCURIE = Union[ReferenceTuple, NonePair, None]

DISALLOWED_EMAIL_PARTS = {
    "contact@",
    "help@",
    "helpdesk@",
    "discuss@",
    "support@",
}


class FailureReturnType(enum.Enum):
    """A flag for what to return when handling reference tuples."""

    #: return a single None
    single = enum.auto()
    #: return a pair of None's
    pair = enum.auto()


def get_failure_return_type(frt: FailureReturnType) -> None | NonePair:
    """Get the right failure return type."""
    if frt == FailureReturnType.single:
        return None
    elif frt == FailureReturnType.pair:
        return None, None
    raise TypeError
