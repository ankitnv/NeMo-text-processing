# Copyright (c) 2023, NVIDIA CORPORATION & AFFILIATES.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os


def get_abs_path(rel_path):
    """
    Get absolute path

    Args:
        rel_path: relative path to this file
<<<<<<< HEAD
<<<<<<< HEAD

=======
        
>>>>>>> 0a4a21c (Jp itn 20240221 (#141))
=======

>>>>>>> 59f46198ab4c8880c6a5fb88f3cbee9530156498
    Returns absolute path
    """
    return os.path.dirname(os.path.abspath(__file__)) + '/' + rel_path
