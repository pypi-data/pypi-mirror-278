"""
Copyright (c) 2024 Pierre-Yves Genest.

This file is part of ParaCopy.

ParaCopy is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, version 3 of the
License.

ParaCopy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with ParaCopy. If not, see <https://www.gnu.org/licenses/>.
"""

from typing import List, Optional
import os
import io
import re
import site
import subprocess
import asyncio


def regex_readlines(wrapper: io.TextIOWrapper, endline: re.Pattern, n: int):
    """Readline with regex
    Args:
        wraper (io.TextIOWrapper): wraper to read
        regex (re.Pattern): regex to match endline
        n (int): buffer
    Yields:
        str: line
    """
    previous_line = ""
    finished = False
    while not finished:
        current_read = wrapper.read(n).decode()
        previous_line += current_read
        splitted = endline.split(previous_line)
        previous_line = splitted[-1]
        if len(splitted) > 1:
            for line in splitted[:-1]:
                yield line
        if current_read == "":
            finished = True


def ensure_root(args: List[str], cwd: Optional[str] = None) -> List[str]:
    """Ensure program will be run as root
    Args:
        args (List[str]): args
        cwd (Optional[str]): current working directory to use
    Returns:
        List[str]: modified args to run as root
    """
    # Adding PYTHONPATH
    pythonpath = []
    if cwd is not None:  # Add current working directory
        pythonpath.append(cwd)
    if os.geteuid() != 0:  # Add user installed packages
        pythonpath.append(site.USER_SITE)
    if len(pythonpath) > 0:
        args = ["/usr/bin/env", f"PYTHONPATH={':'.join(pythonpath)}:$PYTHONPATH"] + args

    # Adding root command
    if os.geteuid() != 0:
        args = ["/bin/pkexec"] + args

    return args


async def async_subprocess_check_call(*args, **kwargs):
    """Async equivalent of subprocess check_call
    Args:
        asyncio.create_subprocess_exec
    Returns:
        None
    """
    proc = await asyncio.create_subprocess_exec(*args, **kwargs)
    return_code = await proc.wait()
    if return_code != 0:
        raise subprocess.CalledProcessError(return_code, args)


async def async_subprocess_check_output(*args, **kwargs):
    """Async equivalent of subprocess check_output
    Args:
        asyncio.create_subprocess_exec
    Returns:
        None
    """
    proc = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, **kwargs
    )
    stdout_data, _ = await proc.communicate()
    if proc.returncode != 0:
        raise subprocess.CalledProcessError(proc.returncode, args)
    else:
        return stdout_data


async def async_subprocess_run(*args, **kwargs):
    """Async equivalent of subprocess run
    Args:
        asyncio.create_subprocess_exec
    Returns:
        None
    """
    proc = await asyncio.create_subprocess_exec(*args, **kwargs)
    await proc.wait()
