from setuptools import setup

# read the contents of your README file
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name="sharedkernel",
    author="Smilinno",
    packages=[
        "sharedkernel",
        "sharedkernel.database",
        "sharedkernel.database.vector_database_repository",
        "sharedkernel.enum",
        "sharedkernel.exception",
        "sharedkernel.objects",
    ],
    # Needed for dependencies
    install_requires=[
        "numpy",
        "requests",
        "pymongo",
        "fastapi==0.89.1",
        "PyJWT",
        "pymilvus",
        "chromadb",
        "persian_tools",
        "sentry-sdk",
    ],
    # *strongly* suggested for sharing
    version="1.3.0",
    description="sharekernel is an shared package between all python projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
