# pisek  - Tool for developing tasks for programming competitions.
#
# Copyright (c)   2019 - 2022 Václav Volhejn <vaclav.volhejn@gmail.com>
# Copyright (c)   2019 - 2022 Jiří Beneš <mail@jiribenes.com>
# Copyright (c)   2020 - 2022 Michal Töpfer <michal.topfer@gmail.com>
# Copyright (c)   2022        Jiří Kalvoda <jirikalvoda@kam.mff.cuni.cz>
# Copyright (c)   2023        Daniel Skýpala <daniel@honza.info>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import filecmp
import glob
from math import ceil
import os
import shutil
from typing import Any, Callable, Iterable, Literal

import subprocess
from pisek.env.env import Env
from pisek.config.task_config import ProgramLimits
from pisek.utils.paths import TaskPath
from pisek.utils.terminal import colored_env
from pisek.utils.text import tab
from pisek.config.task_config import SubtaskConfig, ProgramType
from pisek.jobs.jobs import Job
from pisek.jobs.status import StatusJobManager


TOOLS_MAN_CODE = "tools"
GENERATOR_MAN_CODE = "generator"
INPUTS_MAN_CODE = "inputs"
CHECKER_MAN_CODE = "checker"
JUDGE_MAN_CODE = "judge"
SOLUTION_MAN_CODE = "solution_"
DATA_MAN_CODE = "data"


class TaskHelper:
    _env: Env

    def _get_seed(self, input_name: str):
        """Get seed from input name."""
        parts = os.path.splitext(os.path.basename(input_name))[0].split("_")
        if len(parts) == 1:
            return "0"
        else:
            return parts[-1]

    def _get_limits(self, program_type: ProgramType) -> dict[str, Any]:
        """Get execution limits for given program type."""
        limits: ProgramLimits = getattr(self._env.config.limits, program_type.name)
        time_limit = limits.time_limit

        if program_type in (ProgramType.solve, ProgramType.sec_solve):
            if self._env.timeout is not None:
                time_limit = self._env.timeout

        return {
            "time_limit": time_limit,
            "clock_limit": limits.clock_limit(time_limit),
            "mem_limit": limits.mem_limit,
            "process_limit": limits.process_limit,
        }

    def globs_to_files(
        self, globs: Iterable[str], directory: TaskPath
    ) -> list[TaskPath]:
        """Get files in given directory that match any glob."""
        files: list[str] = sum(
            (glob.glob(g, root_dir=directory.path) for g in globs),
            start=[],
        )
        files = list(sorted(set(files)))
        return [TaskPath.from_abspath(directory.path, file) for file in files]

    @staticmethod
    def _short_text(
        text: str,
        style: Literal["h", "t", "ht"] = "h",
        max_lines: int = 10,
        max_chars: int = 100,
    ) -> str:
        """
        Shorten text to max_lines lines and max_chars on line.
        Keep lines from head / tail / both depending on style.
        """
        s_text = []
        for line in text.split("\n"):
            if len(line) > max_chars:
                line = line[: max_chars - 1] + "…"
            s_text.append(line)
        if len(s_text) < max_lines:
            return "\n".join(s_text)

        tail = max(ceil(("t" in style) * max_lines / len(style)) - 1, 0)
        head = max_lines - tail - 1
        return "\n".join(s_text[:head] + ["[…]"] + (s_text[-tail:] if tail else []))

    @staticmethod
    def makedirs(path: TaskPath, exist_ok: bool = True):
        """Make directories"""
        os.makedirs(path.path, exist_ok=exist_ok)

    @staticmethod
    def make_filedirs(path: TaskPath, exist_ok: bool = True):
        """Make directories for given file"""
        os.makedirs(os.path.dirname(path.path), exist_ok=exist_ok)


class TaskJobManager(StatusJobManager, TaskHelper):
    """JobManager class that implements useful methods"""

    def _get_samples(self) -> list[tuple[TaskPath, TaskPath]]:
        """Returns the list [(sample1.in, sample1.out), …]."""
        ins = self._subtask_inputs(self._env.config.subtasks[0])
        outs = (TaskPath.output_static_file(self._env, inp.name) for inp in ins)
        return list(zip(ins, outs))

    def _all_inputs(self) -> list[TaskPath]:
        """Get all input files"""
        return self.prerequisites_results[INPUTS_MAN_CODE]["inputs"]

    def _subtask_inputs(self, subtask: SubtaskConfig) -> list[TaskPath]:
        """Get all inputs of given subtask."""
        return list(filter(lambda p: subtask.in_subtask(p.name), self._all_inputs()))

    def _subtask_new_inputs(self, subtask: SubtaskConfig) -> list[TaskPath]:
        """Get new inputs of given subtask."""
        return list(
            filter(lambda p: subtask.new_in_subtask(p.name), self._all_inputs())
        )


class TaskJob(Job, TaskHelper):
    """Job class that implements useful methods"""

    @staticmethod
    def _file_access(files: int):
        """Adds first i args as accessed files."""

        def dec(f: Callable[..., Any]) -> Callable[..., Any]:
            def g(self, *args, **kwargs):
                for i in range(files):
                    self._access_file(args[i])
                return f(self, *args, **kwargs)

            return g

        return dec

    @_file_access(1)
    def _open_file(self, filename: TaskPath, mode="r", **kwargs):
        if "w" in mode:
            self.make_filedirs(filename)
        return open(filename.path, mode, **kwargs)

    @_file_access(1)
    def _file_exists(self, filename: TaskPath):
        return os.path.isfile(filename.path)

    @_file_access(1)
    def _file_size(self, filename: TaskPath):
        return os.path.getsize(filename.path)

    @_file_access(1)
    def _file_not_empty(self, filename: TaskPath):
        with self._open_file(filename) as f:
            content = f.read()
        return len(content.strip()) > 0

    @_file_access(2)
    def _copy_file(self, filename: TaskPath, dst: TaskPath):
        self.make_filedirs(dst)
        return shutil.copy(filename.path, dst.path)

    @_file_access(2)
    def _link_file(self, filename: TaskPath, dst: TaskPath, overwrite: bool = False):
        self.make_filedirs(dst)
        if overwrite and os.path.exists(dst.path):
            os.remove(dst.path)
        return os.link(filename.path, dst.path)

    @_file_access(2)
    def _files_equal(self, file_a: TaskPath, file_b: TaskPath) -> bool:
        return filecmp.cmp(file_a.path, file_b.path)

    @_file_access(2)
    def _diff_files(self, file_a: TaskPath, file_b: TaskPath) -> str:
        diff = subprocess.run(
            ["diff", file_a.path, file_b.path, "-Bb", "-u2"],
            stdout=subprocess.PIPE,
        )
        return diff.stdout.decode("utf-8")

    def _quote_file(self, file: TaskPath, **kwargs) -> str:
        """Get shortened file contents"""
        with self._open_file(file) as f:
            return self._short_text(f.read().strip(), **kwargs)

    def _quote_file_with_name(
        self, file: TaskPath, force_content: bool = False, **kwargs
    ) -> str:
        """
        Get file name (with its shortened content if env.file_contents or force_content)
        for printing into terminal
        """
        if force_content or self._env.file_contents:
            return f"{file.col(self._env)}\n{colored_env(tab(self._quote_file(file, **kwargs)), 'yellow', self._env)}\n"
        else:
            return f"{file.col(self._env)}\n"
