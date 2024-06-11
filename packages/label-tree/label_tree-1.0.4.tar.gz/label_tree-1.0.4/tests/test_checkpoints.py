import contextlib
import os
import re

import boto3
import pytest
from dotenv import load_dotenv

from label_tree.diseases_tree import get_all_children, get_all_parents

load_dotenv(override=True)


def list_s3_buckets_with_pattern(pattern: str = "checkpoints"):
    """
    Lists all S3 buckets whose names contain the `pattern`.

    Args:
        pattern: A string to look for in the bucket names and filter by.

    Returns: All bucket names that contain the pattern string.

    """
    s3_client = boto3.client("s3")
    response = s3_client.list_buckets()
    return [
        bucket["Name"] for bucket in response["Buckets"] if pattern in bucket["Name"]
    ]


@pytest.mark.parametrize("bucket_name", list_s3_buckets_with_pattern())
def test_checkpoint_bucket(bucket_name, label_version):

    s3_client = boto3.client("s3")
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    file_names = [obj["Key"] for obj in response.get("Contents", [])]

    # Look for labels
    labels = [
        re.search(r"(?<=GPU\d_).+(?=_epoch)", s).group()
        for s in file_names
        if re.search(r"(?<=GPU\d_).+(?=_epoch)", s)
    ]

    from label_tree.diseases_tree import DiseaseTree

    with open(os.devnull, "w") as null_file, contextlib.redirect_stdout(null_file):
        tree = DiseaseTree(skip_comments=False, label_version=label_version)

    for label in labels:
        if not tree.check_if_diagnosed(tree.get_canonial_form(label)):

            children_diagnosed = any(
                tree.check_if_diagnosed(child)
                for child in get_all_children(tree, label)
            )
            parents_diagnosed = any(
                tree.check_if_diagnosed(parent)
                for parent in get_all_parents(tree, label)
            )

            if not children_diagnosed and not parents_diagnosed:
                raise ValueError(f"Label {label} is not diagnosed")
