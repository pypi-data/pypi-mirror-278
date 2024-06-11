# Copyright (c) 2023-2024 Contributors to the Eclipse Foundation
#
# This program and the accompanying materials are made available under the
# terms of the Apache License, Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# SPDX-License-Identifier: Apache-2.0

import json
import os
import sys
from io import TextIOWrapper
from typing import Any, Callable, Dict, List, Optional

import requests


def to_camel_case(snake_str: str) -> str:
    """Return a camel case version of a snake case string.

    Args:
        snake_str (str): A snake case string.

    Returns:
        str: A camel case version of a snake case string.
    """
    return "".join(x.capitalize() for x in snake_str.lower().split("-"))


def create_truncated_string(input: str, length: int) -> str:
    """Create a truncated version of input if it is longer than length.
    Will keep the rightmost characters and cut of the front if it is
    longer than allowed.

    Args:
        input (str): The input string.
        length (int): The allowed overall length.

    Returns:
        str: A truncated string which has len() of length.
    """
    if len(input) < length:
        return input

    return f"...{input[-length+3:]}"  # noqa: E226 intended behaviour


def replace_in_file(file_path: str, text: str, replacement: str) -> None:
    """Replace all occurrences of text in a file with a replacement.

    Args:
        file_path (str): The path to the file.
        text (str): The text to find.
        replacement (str): The replacement for text.
    """
    buffer = []
    for line in open(file_path, encoding="utf-8"):
        buffer.append(line.replace(text, replacement))

    with open(file_path, mode="w", encoding="utf-8") as file:
        for line in buffer:
            file.write(line)


def get_valid_arch(arch: str) -> str:
    """Return a known architecture for the given `arch`.

    Args:
        arch (str): The architecture of the profile.

    Returns:
        str: valid architecture.
    """
    if "x86_64" in arch or "amd64" in arch:
        return "x86_64"
    elif "aarch64" in arch or "arm64" in arch:
        return "aarch64"

    raise ValueError(f"Unknown architecture: {arch}")


def capture_textfile_area(
    file: TextIOWrapper,
    start_line: str,
    end_line: str,
    map_fn: Optional[Callable[[str], str]] = None,
) -> List[str]:
    """Capture an area of a textfile between a matching start line (exclusive) and the first line matching end_line (exclusive).

    Args:
        file (TextIOWrapper): The text file to read from.
        start_line (str): The line which triggers the capture (will not be part of the output)
        end_line (str): The line which terminates the capture (will not be bart of the output)
        map_fn (Optional[Callable[[str], str]], optional): An optional mapping function to transform captured lines. Defaults to None.

    Returns:
        List[str]: A list of captured lines.
    """
    area_content: List[str] = []
    is_capturing = False
    for line in file:
        if line.strip() == start_line:
            is_capturing = True
        elif line.strip() == end_line:
            is_capturing = False
        elif is_capturing:
            line = line.rstrip()

            if map_fn:
                line = map_fn(line)

            area_content.append(line)
    return area_content


def require_env(name: str) -> str:
    """Require and return an environment variable.

    Args:
        name (str): The name of the variable.

    Raises:
        ValueError: In case the environment variable is not set.

    Returns:
        str: The value of the variable.
    """
    var = os.getenv(name)
    if not var:
        raise ValueError(f"Environment variable {name!r} not set!")
    return var


def get_workspace_dir() -> str:
    """Return the workspace directory."""
    return require_env("VELOCITAS_WORKSPACE_DIR")


def get_app_manifest() -> Dict[str, Any]:
    manifest_data = json.loads(require_env("VELOCITAS_APP_MANIFEST"))
    if isinstance(manifest_data, dict):
        return manifest_data
    elif isinstance(manifest_data, list) and isinstance(manifest_data[0], dict):
        return manifest_data[0]
    else:
        raise TypeError("Manifest must be a dict or array!")


def get_script_path() -> str:
    """Return the absolute path to the directory the invoked Python script
    is located in."""
    return os.path.dirname(os.path.realpath(sys.argv[0]))


def get_package_path() -> str:
    """Return the absolute path to the package directory the invoked Python
    script belongs to."""
    return require_env("VELOCITAS_PACKAGE_DIR")


def get_project_cache_dir() -> str:
    """Return the project's cache directory.

    Returns:
        str: The path to the project's cache directory.
    """
    return require_env("VELOCITAS_CACHE_DIR")


def get_cache_data() -> Dict[str, Any]:
    """Return the data of the cache as Python object."""
    cache_data = json.loads(require_env("VELOCITAS_CACHE_DATA"))

    if not isinstance(cache_data, dict):
        raise TypeError("VELOCITAS_CACHE_DATA has to be a JSON object!")

    return cache_data


def get_log_file_name(service_id: str, runtime_id: str) -> str:
    """Build the log file name for the given service and runtime.

    Args:
        service_id (str): The ID of the service to log.
        runtime_id (str): The ID of the runtime to log.

    Returns:
        str: The log file name.
    """
    return os.path.join(get_workspace_dir(), "logs", runtime_id, f"{service_id}.log")


def get_programming_language() -> str:
    """Return the programming language of the project."""
    return require_env("language")


def create_log_file(service_id: str, runtime_id: str) -> TextIOWrapper:
    """Create a log file for the given service and runtime.

    Args:
        service_id (str): The ID of the service to log.
        runtime_id (str): The ID of the runtime to log.

    Returns:
        TextIOWrapper: The log file.
    """
    log_file_name = get_log_file_name(service_id, runtime_id)
    os.makedirs(os.path.dirname(log_file_name), exist_ok=True)
    return open(log_file_name, "w", encoding="utf-8")


def download_file(uri: str, local_file_path: str) -> None:
    with requests.get(uri, timeout=30) as infile:
        os.makedirs(os.path.split(local_file_path)[0], exist_ok=True)
        with open(local_file_path, "wb") as outfile:
            for chunk in infile.iter_content(chunk_size=8192):
                outfile.write(chunk)
