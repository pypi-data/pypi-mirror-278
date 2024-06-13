# This file is part of fm-actor, a library for interacting with fm-data files:
# https://gitlab.com/sosy-lab/software/fm-actor
#
# SPDX-FileCopyrightText: 2024 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: MIT

import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from tempfile import (
    NamedTemporaryFile,
    mkdtemp,
)
from typing import Any, Dict, List, Optional, Sequence, Tuple

from werkzeug.utils import secure_filename

from fm_tools.download import (
    DownloadDelegate,
    _download_into_file,
    download_into,
    is_download_qualified_url,
)
from fm_tools.exceptions import (
    EmptyVersionException,
    InvalidDataException,
    MissingKeysException,
    VersionConflictException,
)
from fm_tools.files import unzip
from fm_tools.run import Limits, command_line, get_executable_path
from fm_tools.zenodo import get_archive_url_from_zenodo_doi


@dataclass(frozen=True)
class ArchiveLocation:
    raw: str
    resolved: Optional[str] = None

    def resolve(self) -> "ArchiveLocation":
        if self.resolved is not None:
            return self

        resolved = get_archive_url_from_zenodo_doi(self.raw)
        return ArchiveLocation(self.raw, resolved)


@dataclass()
class ToolInfoModule:
    """
    Tool-info-modules in fm-tools have one of three forms:
        - a URL to a python file
        - The fully qualified name of a python module, i.e. benchexec.tools.<toolname>
        - The name of a tool in the benchexec.tools namespace, i.e. <toolname>[.py]
    benchexec supports the latter two. In the first case, the ToolInfoModule must be downloaded beforehand.
    """

    raw: str
    resolved: Optional[str] = None
    _propagate_delete = False
    _target_location: Optional[Path] = None

    def __init__(self, raw: str):
        self.raw = raw

    def _trivially_resolved(self):
        if self.resolved is not None:
            return self

        if not is_download_qualified_url(self.raw):
            # The tool-info-module is already a valid module name
            if self.raw.endswith(".py"):
                self.resolved = self.raw.rpartition(".")[0]
            else:
                self.resolved = self.raw
            return self

        return None

    def resolve(self, target_dir=None, delegate=None) -> "ToolInfoModule":
        """
        Download the tool-info-module if necessary.
        If target_dir is not used, the module is downloaded into a temporary file.
        """
        delegate = delegate or DownloadDelegate()

        if self._trivially_resolved() is not None:
            return self

        if target_dir is None:
            target_dir = Path(mkdtemp(prefix="toolinfo_"))
            self._propagate_delete = True

        if target_dir.is_file():
            raise FileExistsError("The target directory is a file.")

        target_dir.mkdir(parents=True, exist_ok=True)
        file_name = self.raw.rpartition("/")[-1]
        self._target_location = target = target_dir / file_name
        with target.open("wb") as f:
            _download_into_file(self.raw, f, delegate=delegate)

        self.resolved = "." + target.stem
        return self

    def make_available(self):
        """
        Make the resolved tool-info-module available for import.
        If necessary the tool-info-module is downloaded into a temporary file.
        """
        self.resolve()
        if self._target_location:
            sys.path.insert(0, str(self._target_location.parent))

    def __str__(self):
        return self.resolved or self.raw

    def __del__(self):
        if self._propagate_delete:
            shutil.rmtree(self._target_location.parent)

    def __bool__(self):
        if self._trivially_resolved() is not None:
            return True
        return self.resolved is None


@dataclass(frozen=True)
class FmImageConfig:
    base_images: Tuple[str, ...]
    full_images: Tuple[str, ...]
    required_packages: Tuple[str, ...]

    def with_fallback(self, image: str | None):
        """
        Returns a new FmImageConfig with the given image as the base image if the base image is not set.
        """

        return FmImageConfig(
            self.base_images or (image,),
            self.full_images,
            self.required_packages,
        )


class FmData:

    def __init__(
        self,
        config: Dict[str, Any],
        version: Optional[str] = None,
    ):
        self._config = config
        self._check_fm_data_integrity()

        self.actor_name = self._safe_name_from_config(version)

        self.version = self._find_version_from_given(version)

        self._version_specific_config = self._find_version_specific_config(
            config.get("versions", [])
        )

        self.options = self._version_specific_config.get(
            "benchexec_toolinfo_options", []
        )

        self.archive_location = self._prepare_archive_location()

    def _safe_name_from_config(self, version: Optional[str]) -> str:
        return secure_filename(self._config["name"] + f"-{version if version else ' '}")

    def _find_version_from_given(self, version: Optional[str]):
        if not version:
            try:
                return self._config["versions"][0]["version"]
            except (IndexError, KeyError) as e:
                raise InvalidDataException(
                    f"There are no versions specified in {self.get_actor_name()}"
                ) from e

        return version

    def _find_version_specific_config(self, versions):
        tool_configs = [x for x in versions if str(x["version"]) == self.get_version()]

        if len(tool_configs) < 1:
            raise VersionConflictException(
                f"Version {self.get_version()} not found for actor {self.get_actor_name()}"
            )
        if len(tool_configs) > 1:
            raise VersionConflictException(
                "There a multiple versions in the yaml file with the same name!", 2
            )
        tool_config = tool_configs[0]

        if tool_config is None:
            raise EmptyVersionException(
                f'{self.get_actor_name()} doesn\'t recognize the requested version "{self.get_version()}"!'
            )
        return tool_config

    def _check_tool_sources(self, tool_config):
        has_doi = "doi" in tool_config
        has_url = "url" in tool_config

        if not (has_url or has_doi):
            raise InvalidDataException(
                "The actual tool is missing (no URL or DOI of a tool archive)"
            )
        if has_url and has_doi:
            raise InvalidDataException(
                "Two tool archives provided (one by a URL, one by a DOI), it is unclear which one should be used"
            )

        return has_url, has_doi

    def _prepare_archive_location(self):
        tool_config = self._version_specific_config
        has_url, has_doi = self._check_tool_sources(tool_config)

        if has_doi:
            doi = tool_config["doi"]
            return ArchiveLocation(doi)

        if has_url:
            return ArchiveLocation(tool_config["url"], tool_config["url"])

    def download_and_install_into(
        self,
        target_dir: Path,
        delegate: DownloadDelegate = None,
        show_loading_bar: bool = True,
    ):
        """
        Downloads and installs the associated archive into `target_dir`.
        The `target_dir` must not be '/' or '/tmp' to avoid accidental deletion of the system.

        """
        delegate = delegate or DownloadDelegate()

        with NamedTemporaryFile("+wb", suffix=".zip", delete_on_close=True) as tmp:
            archive = Path(tmp.name)
            self.download_into(
                archive, delegate=delegate, show_loading_bar=show_loading_bar
            )
            return self.install_from(archive, target_dir)

    def download_into(
        self,
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

        download_into(self, target, delegate, show_loading_bar)

    def install_from(self, archive_dir: Path, target_dir: Path):
        return unzip(archive_dir, target_dir)

    # implement abstract methods
    def get_archive_location(self) -> ArchiveLocation:
        return self.archive_location

    def get_toolinfo_module(self) -> ToolInfoModule:
        if not hasattr(self, "_tool_info"):
            self._tool_info = ToolInfoModule(self._config["benchexec_toolinfo_module"])
        return self._tool_info

    def get_version(self) -> str:
        return self.version

    def get_options(self) -> List[str]:
        return self.options

    def get_actor_name(self) -> str:
        return self.actor_name

    def _find_key(self, key, default):
        top_level = self._config.get(key, default)
        return self._version_specific_config.get(key, top_level)

    def get_images(self) -> FmImageConfig:
        # Top level images
        base_images = tuple(self._find_key("base_container_images", tuple()))
        full_images = tuple(self._find_key("full_container_images", tuple()))
        required_packages = tuple(self._find_key("required_packages", tuple()))

        return FmImageConfig(base_images, full_images, required_packages)

    def command_line(
        self,
        tool_dir: Path,
        input_files: Optional[Sequence[Path]] = None,
        working_dir: Optional[Path] = None,
        property: Optional[Path] = None,
        options: Optional[List[str]] = None,
        add_options_from_fm_data: bool = False,
        limits: Optional[Limits] = None,
    ) -> List[str]:
        return command_line(
            self,
            tool_dir,
            input_files,
            working_dir,
            property,
            options,
            add_options_from_fm_data,
            limits,
        )

    def get_executable_path(self, tool_dir: Path) -> Path:
        return get_executable_path(self, tool_dir)

    def _check_fm_data_integrity(self):
        # check if the essential tags are present.
        # Essentiality of tags can be defined in a schema.
        essential_tags = {
            "benchexec_toolinfo_module",
            "name",
            "versions",
        }
        diff = essential_tags - self._config.keys()
        if diff:
            raise MissingKeysException(diff)
