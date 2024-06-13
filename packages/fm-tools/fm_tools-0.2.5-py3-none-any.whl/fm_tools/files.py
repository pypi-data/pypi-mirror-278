# This file is part of fm-actor, a library for interacting with fm-data files:
# https://gitlab.com/sosy-lab/software/fm-actor
#
# SPDX-FileCopyrightText: 2024 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: MIT

import os
import shutil
from pathlib import Path
from typing import IO, Iterator
from zipfile import ZipFile, ZipInfo


def unzip(archive: Path | str | IO[bytes], target_dir: Path):
    if target_dir.is_dir():
        shutil.rmtree(target_dir)

    with ZipFile(archive, "r") as zipfile:
        root_dir_amount = len(
            {
                member.filename.split("/")[0]
                for member in zipfile.filelist
                if member.filename.count("/") <= 1
            }
        )
        if root_dir_amount != 1:
            raise ValueError(
                f"Archive structure is not supported!\n"
                "Exactly one top level directory expected,"
                f" {root_dir_amount} were given."
            )

        top_level_zip_folder = zipfile.filelist[0].filename.split("/")[0]
        top_folder = target_dir.parent / top_level_zip_folder
        # Not to use extract all as it does not preserves the permission for executable files.
        # See: https://bugs.python.org/issue15795
        # See https://stackoverflow.com/questions/39296101/python-zipfile-removes-execute-permissions-from-binaries
        for member in zipfile.namelist():
            if not isinstance(member, ZipInfo):
                member = zipfile.getinfo(member)
            extracted_file = zipfile.extract(member, target_dir.parent)
            # This takes first two bytes from four bytes.
            attr = member.external_attr >> 16
            if attr != 0:
                os.chmod(extracted_file, attr)
        top_folder.rename(target_dir)


def write_file_from_iterator(target_path: Path, content_iter: Iterator[bytes]):
    with target_path.open("wb") as out_file:
        for data in content_iter:
            out_file.write(data)
