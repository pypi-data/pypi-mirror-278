import setuptools
import subprocess
import os

mdoutline_version = (
    subprocess.run(["git", "describe", "--tags"], stdout=subprocess.PIPE)
    .stdout.decode("utf-8")
    .strip()
)

if "-" in mdoutline_version:
    # when not on tag, git describe outputs: "1.3.3-22-gdf81228"
    # pip has gotten strict with version numbers
    # so change it to: "1.3.3+22.git.gdf81228"
    # See: https://peps.python.org/pep-0440/#local-version-segments
    v,i,s = mdoutline_version.split("-")
    mdoutline_version = v + "+" + i + ".git." + s

assert "-" not in mdoutline_version
assert "." in mdoutline_version

assert os.path.isfile("mdoutline/version.py")
with open("mdoutline/VERSION", "w", encoding="utf-8") as fh:
    fh.write("%s\n" % mdoutline_version)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt') as fh:
    requirements = fh.read().splitlines()

setuptools.setup(
    name="mdoutline",
    version=mdoutline_version,
    author="Rishiraj Acharya",
    author_email="heyrishiraj@gmail.com",
    description="📝",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rishiraj/mdoutline",
    packages=setuptools.find_packages(),
    package_data={"mdoutline": ["VERSION"]},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    entry_points={"console_scripts": ["mdoutline = mdoutline.main:main"]},
    install_requires=requirements,
)