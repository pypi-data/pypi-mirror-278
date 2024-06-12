# This file is part of fm-actor, a library for interacting with fm-data files:
# https://gitlab.com/sosy-lab/software/fm-actor
#
# SPDX-FileCopyrightText: 2024 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: MIT


class FmDataException(Exception): ...


class ToolInfoNotResolvedError(FmDataException): ...


class DownloadUnsuccessfulException(FmDataException): ...


class InvalidDataException(FmDataException): ...


class UnsupportedDOIException(InvalidDataException): ...


class MissingKeysException(FmDataException): ...


class VersionConflictException(FmDataException): ...


class EmptyVersionException(VersionConflictException): ...
