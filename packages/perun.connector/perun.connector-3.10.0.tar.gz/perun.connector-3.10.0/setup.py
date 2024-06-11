import setuptools


def readme():
    with open("README.md") as f:
        return f.read()


setuptools.setup(
    name="perun.connector",
    python_requires=">=3.9",
    url="https://gitlab.ics.muni.cz/perun/perun-proxyidp/perun-connector.git",
    description="Module for high-volume communication with Perun IdM",
    long_description=readme(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_namespace_packages(include=["perun.*"]),
    install_requires=[
        "setuptools",
        "urllib3~=1.26",
        "python-dateutil~=2.8",
        "PyYAML~=6.0",
        "ldap3~=2.9",
        "jsonpatch~=1.22",
    ],
)
