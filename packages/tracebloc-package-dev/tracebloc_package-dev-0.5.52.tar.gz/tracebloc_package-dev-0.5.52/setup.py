from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="tracebloc_package-dev",
    version="0.5.52",
    description="Package required to run Tracebloc jupyter notebook to create experiment",
    url="https://gitlab.com/tracebloc/tracebloc-py-package/-/tree/dev",
    license="MIT",
    python_requires=">=3",
    packages=find_packages(),
    author="Tracebloc",
    author_email="info@tracebloc.io",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "absl-py",
        "dill==0.3.7",
        "protobuf",
        "requests",
        "rich",
        "silence-tensorflow==1.2.1",
        "tensorflow",
        "tensorflow-datasets",
        "termcolor",
        "timm==0.9.10",
        "torch",
        "torchlightning==0.0.0",
        "torchmetrics==1.2.0",
        "torchvision",
        "tqdm",
        "transformers",
        "twine==4.0.1",
    ],
    zip_safe=False,
)
