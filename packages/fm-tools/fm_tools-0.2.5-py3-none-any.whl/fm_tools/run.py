# This file is part of fm-actor, a library for interacting with fm-data files:
# https://gitlab.com/sosy-lab/software/fm-actor
#
# SPDX-FileCopyrightText: 2024 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass
from functools import cache
from pathlib import Path
from typing import TYPE_CHECKING, List, Optional, Sequence

from benchexec.tools.template import BaseTool2

from fm_tools.exceptions import ToolInfoNotResolvedError

from .benchexec_helper import load_tool_info

if TYPE_CHECKING:
    from benchexec.tools.template import BaseTool2

    from .fmdata import FmData


@dataclass(frozen=True)
class Limits:
    """
    Dataclass representing the desired limits for the execution of a tool.
    The limits *are not enforced nor guaranteed*. They merely serve as optional
    data that is used while generating the command line for a tool.

    """

    cpu_time: Optional[int] = None
    wall_time: Optional[int] = None
    memory: Optional[int] = None
    cores: Optional[int] = None

    def as_benchexec_limits(self) -> "BaseTool2.ResourceLimits":
        from benchexec.tools.template import BaseTool2

        return BaseTool2.ResourceLimits(
            cputime=self.cpu_time,
            cputime_hard=self.cpu_time,
            walltime=self.wall_time,
            memory=self.memory,
            cpu_cores=self.cores,
        )


@cache
def get_tool_info(fm_data: "FmData"):
    try:
        _, tool = load_tool_info(str(fm_data.get_toolinfo_module()))
        return tool
    except (ImportError, ModuleNotFoundError) as e:
        raise ToolInfoNotResolvedError(
            "Could not load toolinfo module. "
            "Make sure it is available in the sys.path, e.g., by calling the make_available() method. "
            f"Original error was: {repr(e)}"
        ) from e


def get_executable_path(fm_data: "FmData", tool_dir: Path):

    locator = BaseTool2.ToolLocator(tool_directory=tool_dir)
    tool = get_tool_info(fm_data)
    return tool.executable(locator)


def command_line(
    fm_data: "FmData",
    tool_dir: Path,
    input_files: Sequence[Path],
    working_dir: Optional[Path] = None,
    property: Optional[Path] = None,  # noqa: A002
    options: Optional[List[str]] = None,
    add_options_from_fm_data: bool = False,
    limits: Optional[Limits] = None,
) -> List[str]:

    options = options or []

    if add_options_from_fm_data:
        options = fm_data.get_options() + options

    if not fm_data.get_toolinfo_module():
        raise ToolInfoNotResolvedError(
            "The toolinfo module must be resolved before generating the command line."
        )

    executable = get_executable_path(fm_data, tool_dir)
    tool = get_tool_info(fm_data)

    task = BaseTool2.Task.with_files(input_files, property_file=property)

    rlimits = limits.as_benchexec_limits() if limits else BaseTool2.ResourceLimits()

    return tool.cmdline(executable, options, task, rlimits)
