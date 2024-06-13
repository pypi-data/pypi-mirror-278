# Copyright (c) Meta Platforms, Inc. and affiliates.
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

import argparse
import os
import shutil

import pkg_resources


def main():
    parser = argparse.ArgumentParser(description="Extract Project Aria Client Samples.")
    parser.add_argument(
        "--output", "-o", dest="output", help="Output directory", default=os.getcwd()
    )
    args = parser.parse_args()

    # Location in package install
    samples = pkg_resources.resource_filename("aria", "samples")

    # Destination directory
    output = os.path.join(args.output, "projectaria_client_sdk_samples")

    if os.path.exists(output):
        prompt = (
            f"Directory {output} already exists, would you like to replace it? [y/N]: "
        )
        if input(prompt).lower().strip() == "y":
            print(f"Removing existing directory {output}")
            shutil.rmtree(output)
        else:
            print(f" Not replacing directory, please extract to a different directory")
            exit(1)

    # Copy samples to output directory
    print(f"Extracting samples to {output}")
    shutil.copytree(samples, output)


if __name__ == "__main__":
    main()
