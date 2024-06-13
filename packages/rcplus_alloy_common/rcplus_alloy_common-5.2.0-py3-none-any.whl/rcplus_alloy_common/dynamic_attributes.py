"""
Dynamic attributes related functions

NOTE: S3 related utils implemented here to avoid dependency on `aws` extra which requires
      such heavy dependencies as `pandas` and `awswrangler`.
"""
import os
import re
import math
import logging
from typing import Tuple
from urllib.parse import urlparse

import yaml
import boto3

logger = logging.getLogger(__name__)

REPOSITORY_TAG = os.environ.get("REPOSITORY_TAG")
PROJECT_VERSION = os.environ.get("PROJECT_VERSION")
PROFILES_TAXONOMY_TABLE = "profiles_taxonomy"


class CustomDumper(yaml.SafeDumper):
    # A hackish way to deal with PyYAML formatting, at least to make tables definitions visually separated
    # inspired by https://stackoverflow.com/a/44284819/3786245
    def write_line_break(self, data=None):
        super().write_line_break(data)

        if len(self.indents) == 1:
            super().write_line_break()

        if len(self.indents) == 4:
            super().write_line_break()


def parse_s3_url(s3_url) -> Tuple[str, str]:
    """
    Parse S3 URL and return (S3 bucket, S3 path) tuple pair on success or raise ValueError exception
    """
    url_parts = urlparse(s3_url)
    if url_parts.scheme != "s3" or url_parts.netloc is None or url_parts.path is None:
        raise ValueError(f"Failed to parse malformed S3 URL {s3_url}")

    return url_parts.netloc, url_parts.path.lstrip("/")


def read_s3_file_content(s3_url):
    """
    Read S3 file content into memory
    """
    s3 = boto3.client("s3")
    s3_bucket, s3_path = parse_s3_url(s3_url)

    logger.debug(f"Read S3 file content from {s3_url}")
    return s3.get_object(Bucket=s3_bucket, Key=s3_path)["Body"].read().decode("utf-8")


def normalize_label(label_name: str, attribute_name: str) -> str:
    """
    Some arbitrary rules based on our current experience:
    - a label can't start with a digit, so prefix it with its attribute name
    - a label can't have `-` (hyphen), so replace it with `_` (underscore)
    - a label can't have `+`, so replace it with `_plus` text
    Probably some more rules will be applied in the future
    """
    if re.match(r"^\d", label_name):
        label_name = f"{attribute_name}_{label_name}"

    if "-" in label_name:
        label_name = label_name.replace("-", "_")

    if "+" in label_name:
        label_name = label_name.replace("+", "_plus")

    return label_name


def generate_dynamic_attributes_sources(predictions: list[dict]) -> dict | None:
    """
    Generate dynamic attributes sources definitions based on the `predictions` section from
    the tenants configs file as YAML string
    """
    if not predictions:
        logger.debug("No dynamic attributes sources were generated because predictions are empty")
        return None

    tables = []
    for prediction in predictions:
        params_s3_url = prediction["params_path"]
        params = yaml.safe_load(read_s3_file_content(params_s3_url))
        attr_name = params["task"]["name"]
        logger.debug(f"Generate dynamic attributes sources for {attr_name} based on params from {params_s3_url}")
        labels_str = ",".join([f"{normalize_label(label, attr_name)}:float" for label in params["data"]["labels"]])
        table_name = f"predictions_{attr_name}"

        # The main dynamic attribute table definition
        tables.append({
            "name": table_name,
            "description": f"{attr_name} predictions".capitalize(),
            "columns": [
                {
                    "name": "fp_id",
                    "type": "string",
                    "description": "First party id",
                    "meta": {
                        "pii": True
                    }
                },
                {
                    "name": "predictions",
                    "type": f"struct<{labels_str}>",
                    "description": f"{attr_name} predictions".capitalize(),
                }
            ],
            "external": {
                "partitions": [
                    {
                        "name": "p_timestamp",
                        "type": "timestamp",
                        "description": "Timestamp truncated to an hour when data were processed"
                    },
                ]
            },
            "meta": {
                "repo": REPOSITORY_TAG,
                "source": REPOSITORY_TAG,
                "version": PROJECT_VERSION,
                "depends_on": [f"{table_name}_tmp"]
            },
        })

        # The tmp dynamic attribute table definition (the same as a main table)
        tables.append({
            "name": f"{table_name}_tmp",
            "description": f"{attr_name} predictions".capitalize(),
            "columns": [
                {
                    "name": "fp_id",
                    "type": "string",
                    "description": "First party id",
                    "meta": {
                        "pii": True
                    }
                },
                {
                    "name": "predictions",
                    "type": f"struct<{labels_str}>",
                    "description": f"{attr_name} predictions".capitalize(),
                }
            ],
            "external": {
                "partitions": [
                    {
                        "name": "p_timestamp",
                        "type": "timestamp",
                        "description": "Timestamp truncated to an hour when data were processed"
                    },
                ]
            },
            "meta": {
                "repo": REPOSITORY_TAG,
                "source": REPOSITORY_TAG,
                "version": PROJECT_VERSION,
                "depends_on": [PROFILES_TAXONOMY_TABLE, f"{table_name}_columns"]
            },
        })

        # The columns dynamic attribute table definition
        tables.append({
            "name": f"predictions_{attr_name}_columns",
            "description": f"{attr_name} predictions columns".capitalize(),
            "columns": [
                {
                    "name": "index",
                    "type": "string",
                    "description": "",
                },
                {
                    "name": "taxonomy",
                    "type": "string",
                    "description": "",
                },
                {
                    "name": "col",
                    "type": "bigint",
                    "description": "",
                },
            ],
            "meta": {
                "repo": REPOSITORY_TAG,
                "source": REPOSITORY_TAG,
                "version": PROJECT_VERSION,
            },
        })

    sources = {
        "version": 2,
        "sources": [{
            "name": "attribute_predictions",
            "description": "Attribute Predictions",
            "schema": '{{ env_var("TENANT", "riad") }}',
            "tables": tables,
        }]
    }

    return sources


def to_yaml(sources):
    return yaml.dump(
        sources, sort_keys=False, indent=2, explicit_start=True,
        default_flow_style=False, width=math.inf, Dumper=CustomDumper,
    )
