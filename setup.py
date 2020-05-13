from setuptools import setup, find_packages
from codecs import open
import yaml

with open("Project", 'r') as stream:
    config = yaml.safe_load(stream)

# config = yaml.loadfile("Project")

with open("README.md") as f:
    long_description = f.read()

setup(
    name=config["public_name"],
    version=config["version"],
    author=config["author"],
    author_email=config["author_email"],
    maintainer=config["maintainer"],
    maintainer_email=config["maintainer_email"],
    url=config["url"],
    description=config["description"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    download_url=config["url"] + "/tarball/" + config["version"],
    license=config["license"],
    keywords=config["keywords"],
    include_package_data=True,
    platforms="",
    classifiers=[],
    install_requires=[],
    packages=find_packages(where=".", exclude=("tests", "tests.*")),
    package_dir={"timecount": "timecount"},
    package_data={},
    data_files=[],
    entry_points={"console_scripts": [], "gui_scripts": []},
    tests_require=[""],
)
