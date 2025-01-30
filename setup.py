"""Build python package distribution
- install package locally: pip install .
- create wheel: python setup.py bdist_wheel
"""

import setuptools
import subprocess

package_base = "keysight_chakra"

branch = subprocess.check_output(["git", "branch", "--show-current"]).strip().decode()
with open("./VERSION", "rt") as fp:
    version = f"{fp.readline().strip()}+{branch}"

# List the packages and their dir mapping:
# "install_destination_package_path": "source_dir_path"
package_dir_map = {
    f"{package_base}": "./keysight_chakra",
    f"{package_base}/protobuf": "./keysight_chakra/protobuf",
    f"{package_base}/tests": "./keysight_chakra/tests",
}

requires = [
    "protobuf",
    "pyyaml",
]

setuptools.setup(
    name=package_base,
    version=version,
    python_requires=">=3.8",
    author="Keysight",
    author_email=f"support.ix@keysight.com",
    url="https://github.com/Keysight/infrastructure",
    packages=set(package_dir_map.keys()),
    package_dir=package_dir_map,
    include_package_data=True,
    install_requires=requires,
)
