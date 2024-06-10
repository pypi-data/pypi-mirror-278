"""Chain-code file I/O functions"""

# Copyright 2024 Koji Noshita
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def read_chc(file_path):
    """Read chain-code from a file

    Parameters
    ==========
    file_path: str
        path to the chain-code file (.chc)

    Returns
    =======
    x: Coordinate values converted from chain-code
    """
    with open(file_path, "r") as f:
        chc = f.readlines()

    return x
