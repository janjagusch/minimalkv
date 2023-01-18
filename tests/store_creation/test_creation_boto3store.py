import base64
import json
import os
import pathlib
from uuid import uuid4

import pytest

from minimalkv._get_store import get_store, get_store_from_url
from minimalkv._old_store_creation import create_store
from minimalkv._old_urls import url2dict
from minimalkv.net.gcstore import GoogleCloudStore
from minimalkv.net.s3fsstore import S3FSStore
from tests.bucket_manager import boto3_bucket_reference

storage = pytest.importorskip("google.cloud.storage")
from google.auth.credentials import AnonymousCredentials
from google.auth.exceptions import RefreshError

S3_URL = "s3://minio:miniostorage@127.0.0.1:9000/bucketname?create_if_missing=true&is_secure=false"

"""
When using the `s3` scheme in a URL, the new store creation returns an `S3FSStore`.
The old store creation returns a `BotoStore`.
To compare these two implementations, the following tests are run. 
"""

def test_new_s3fs_creation():
    expected = S3FSStore(
        bucket=boto3_bucket_reference(
            access_key="minio",
            secret_key="miniostorage",
            host="127.0.0.1",
            port=9000,
            bucket_name="bucketname-minio",
            is_secure=False,
        ),
    )

    actual = get_store_from_url(S3_URL)
    assert actual == expected


def test_equal_access():
    new_store = get_store_from_url(S3_URL)
    old_store = get_store(**url2dict(S3_URL))

    new_store.put("key", b"value")
    assert old_store.get("key") == b"value"
