# This file is part of fm-actor, a library for interacting with fm-data files:
# https://gitlab.com/sosy-lab/software/fm-actor
#
# SPDX-FileCopyrightText: 2024 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: MIT

from typing import Iterator, Protocol, Union

import httpx


class RequestsResponse(Protocol):

    __attrs__ = [
        "_content",
        "status_code",
        "headers",
        "url",
        "history",
        "encoding",
        "reason",
        "cookies",
        "elapsed",
        "request",
    ]

    def __init__(self): ...

    def __enter__(self): ...

    def __exit__(self, *args): ...

    def __getstate__(self): ...

    def __setstate__(self, state): ...

    def __repr__(self): ...

    def __bool__(self): ...

    def __nonzero__(self): ...

    def __iter__(self): ...

    @property
    def ok(self): ...

    @property
    def is_redirect(self): ...

    @property
    def is_permanent_redirect(self): ...

    @property
    def next(self): ...  # noqa: A003

    @property
    def apparent_encoding(self): ...

    def iter_content(
        self, chunk_size=1, decode_unicode=False
    ) -> Iterator[bytes] | Iterator[str]: ...

    def iter_lines(
        self, chunk_size=1024, decode_unicode=False, delimiter=None
    ) -> Iterator[bytes] | Iterator[str]: ...

    @property
    def content(self): ...

    @property
    def text(self): ...

    def json(self, **kwargs): ...

    @property
    def links(self): ...

    def raise_for_status(self): ...

    def close(self): ...


class RequestsSession(Protocol):

    def get(
        self,
        url: str,
        headers: dict[str, str] = None,
        allow_redirects=False,
        timeout: int = 10,
        **kwargs,
    ) -> "RequestsResponse": ...
    def head(
        self,
        url: str,
        headers: dict[str, str] = None,
        allow_redirects=False,
        timeout: int = 10,
        **kwargs,
    ) -> "RequestsResponse": ...


Response = Union[httpx.Response, RequestsResponse]
Session = Union[httpx.Client, RequestsSession]
