# This file is part of fm-actor, a library for interacting with fm-data files:
# https://gitlab.com/sosy-lab/software/fm-actor
#
# SPDX-FileCopyrightText: 2024 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: MIT

import json
import logging
from typing import Callable

import httpx
from httpx import Response

from fm_tools.exceptions import UnsupportedDOIException

ZENODO_API_URL_BASE = "https://zenodo.org/api/records/"


def get_archive_url_from_zenodo_doi_with_provider(
    doi: str, provider: Callable[[str], Response]
):
    zenodo_record_id = doi.rsplit(".")[-1]
    url = ZENODO_API_URL_BASE + zenodo_record_id
    response = provider(url)

    if response.status_code != 200:
        raise UnsupportedDOIException(
            f"Failed to get the Zenodo record. "
            f"Status code: {response.status_code}, "
            f"URL: {url}"
        )

    data = json.loads(response.content)
    if len(data["files"]) > 1:
        logging.warning(
            "There are more than one file in the Zenodo record. "
            "The first file will be used."
        )

    # the archive URL is the first file's self link
    return data["files"][0]["links"]["self"]


def get_archive_url_from_zenodo_doi(doi):
    return get_archive_url_from_zenodo_doi_with_provider(
        doi, lambda x: httpx.get(x, timeout=30)
    )
