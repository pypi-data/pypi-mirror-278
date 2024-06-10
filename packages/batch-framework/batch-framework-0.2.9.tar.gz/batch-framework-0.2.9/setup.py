"""
How to sent this package onto PyPi?

1) Building Package Release Tar:
```python setup.py sdist```

2) Upload Package to PyPi:
```pip install twine```
```twine upload dist/*```
"""
import pathlib
import setuptools
from setuptools import find_packages

with open("README.md", "r") as fh:

    long_description = fh.read()

HOME = str(pathlib.Path(__file__).parent.absolute())

with open(HOME +
          "/batch_framework/version.py", "r") as fh:
    version = fh.read().split("=")[1].replace("'", "")

setuptools.setup(

    name="batch-framework",

    version=version,

    author="jeffreylin",

    author_email="jeffrey82221@gmail.com",

    description="Generate Batch Framework",

    long_description=long_description,

    long_description_content_type="text/markdown",

    url="https://github.com/jeffrey82221/batch_framework",

    packages=find_packages(exclude=('tests',)),

    classifiers=[

        "Programming Language :: Python :: 3",

        "License :: OSI Approved :: MIT License",

        "Operating System :: OS Independent",

    ],
    python_requires='>=3.8, !=3.11.*',
    install_requires=[
        'pandas',
        'dropbox',
        'pyarrow',
        'duckdb',
        'paradag',
        'dill',
        'dropboxdrivefs==1.4.1',
        'typing_extensions',
        'vaex',
        'tqdm',
        'types-PyYAML',
        'PyYAML',
        'split-file-reader==0.1.4',
        'urllib3>=2.2.0'
    ]
)
