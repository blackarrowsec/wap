import setuptools
import sys

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

cmdclass = {}
command_options = {}


name = "wap"
version = "0.0.2"

if sys.argv[-1] == "doc":
    # require sphinx only in case of doc command
    from sphinx.setup_command import BuildDoc
    cmdclass["doc"] = BuildDoc
    command_options["doc"] = {
            'project': ('setup.py', name),
            'version': ('setup.py', version),
            'source_dir': ('setup.py', 'docs/source')
    }


setuptools.setup(
    name=name,
    version=version,
    author="Eloy Perez",
    author_email="eloy.perez@tarlogic.com",
    description="Library to parse wappalyzer technologies.json and "
    "extracts matches from HTTP responses",
    url="https://github.com/blackarrowsec/wap",
    project_urls={
        "Repository": "https://github.com/blackarrowsec/wap",
        "Documentation": "https://wap.readthedocs.io",
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    cmdclass=cmdclass,
    command_options=command_options,
)
