# This file is part of fm-actor, a library for interacting with fm-data files:
# https://gitlab.com/sosy-lab/software/fm-actor
#
# SPDX-FileCopyrightText: 2024 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: MIT

from contextlib import contextmanager
from pathlib import Path
from typing import IO, TYPE_CHECKING, Dict, Iterator

import httpx
from tqdm import tqdm

from fm_tools.exceptions import DownloadUnsuccessfulException
from fm_tools.files import write_file_from_iterator

from .types import Response, Session

if TYPE_CHECKING:
    from .fmdata import FmData

DOWNLOAD_CHUNK_SIZE = 4096

_DEFAULT_CLIENT = httpx.Client()


class DownloadDelegate:
    def __init__(self, session: Session = _DEFAULT_CLIENT):
        self.session = session

    @contextmanager
    def stream(
        self, url: str, headers: Dict[str, str], follow_redirects=False, timeout=30
    ):

        try:
            with self.session.stream(
                "GET",
                url,
                headers=headers,
                follow_redirects=follow_redirects,
                timeout=timeout,
            ) as response:
                yield response
        except TypeError:
            response = self.session.get(
                url,
                headers=headers,
                allow_redirects=follow_redirects,
                timeout=timeout,
                stream=True,
            )
            yield response
        finally:
            response.close()

    def get(
        self,
        url: str,
        headers: Dict[str, str],
        follow_redirects=False,
        timeout=30,
    ) -> Response:
        """
        This method wraps both httpx and requests get methods.
        The streaming syntax is different in httpx and requests.
        `.stream` also exists in requests Sessions but it is a boolean,
        thus raising a TypeError if requests is used as `session`.
        Similarly, `follow_redirects` is a known keyword in httpx but
        raises a TypeError in requests.

        """

        try:
            return self.session.get(
                url, headers=headers, follow_redirects=follow_redirects, timeout=timeout
            )
        except TypeError as e:
            print(e)
            # requests
            return self.session.get(
                url,
                headers=headers,
                allow_redirects=follow_redirects,
                timeout=timeout,
                stream=False,
            )

    def head(
        self, url: str, headers: Dict[str, str], follow_redirects=False, timeout=30
    ) -> Response:
        try:
            return self.session.head(
                url, headers=headers, follow_redirects=follow_redirects, timeout=timeout
            )
        except TypeError:
            # requests
            return self.session.head(
                url, headers=headers, allow_redirects=follow_redirects, timeout=timeout
            )


def response_iterator(response: Response) -> Iterator[bytes]:
    try:
        # httpx
        return response.iter_bytes(chunk_size=DOWNLOAD_CHUNK_SIZE)
    except AttributeError:
        # requests
        return response.iter_content(chunk_size=DOWNLOAD_CHUNK_SIZE)


def response_tqdm_iterator(response: Response) -> Iterator[bytes]:

    total = int(response.headers.get("content-length", 0))
    return tqdm(
        response_iterator(response),
        total=int(total / DOWNLOAD_CHUNK_SIZE),
        unit_scale=int(DOWNLOAD_CHUNK_SIZE / 1024),
        unit="KiB",
    )


def is_download_qualified_url(url: str) -> bool:
    return url.startswith("http://") or url.startswith("https://")


def _download_into_file(
    url: str, target: IO[bytes], delegate: DownloadDelegate, timeout=10
) -> None:

    headers = {"User-Agent": "Mozilla"}
    response = delegate.get(
        url, headers=headers, follow_redirects=True, timeout=timeout
    )

    target.write(response.content)


def download_into(
    fm_data: "FmData",
    target: Path,
    delegate: DownloadDelegate = None,
    show_loading_bar: bool = True,
) -> Path:
    """
    Download the associated archive into the given target.
    The target must be a file.
    Rethrows potential exceptions from the session in the download delegate.

    :exception DownloadUnsuccessfulException: if the response code is not 200
    :return: the path to the downloaded archive
    """

    delegate = delegate or DownloadDelegate()

    if not target.parent.exists():
        target.parent.mkdir(parents=True)

    if target.exists() and not target.is_file():
        raise FileExistsError(f"The target path {target} exists and is not a file.")

    headers = {"User-Agent": "Mozilla"}
    url = fm_data.archive_location.resolve().resolved

    with delegate.stream(
        url, follow_redirects=True, headers=headers, timeout=60
    ) as response:
        if response.status_code != 200:
            msg = (
                "Couldn't download contents from: %s. Server returned the code: %s"
                % (
                    str(url),
                    response.status_code,
                )
            )
            raise DownloadUnsuccessfulException(msg)

        response_iter = (
            response_tqdm_iterator(response)
            if show_loading_bar
            else response_iterator(response)
        )
        write_file_from_iterator(target, response_iter)
