# ByMa
![PyPI - Version](https://img.shields.io/pypi/v/byma?style=plastic&label=ByMa&labelColor=green&color=blue&link=https%3A%2F%2Fbytemath.gitlab.io%2Fpython%2FByMa%2Findex.html)
[![PyPI Downloads](https://img.shields.io/pypi/dm/label=PyPI%20downloads)](
https://pypi.org/project/byma/)
[![Conda Downloads](https://img.shields.io/conda/dn/conda-forge/label=Conda%20downloads)](https://anaconda.org/conda-forge/byma)
![Libraries.io dependency status for specific release](https://img.shields.io/librariesio/release/pypi/numpy/1.1.1?style=plastic&logo=numpy&label=NumPy&labelColor=blue&link=https%3A%2F%2Fnumpy.org%2F)
![Libraries.io dependency status for specific release](https://img.shields.io/librariesio/release/pypi/scipy/1.0.0?style=plastic&logo=scipy&label=SciPy&labelColor=light%20blue&link=https%3A%2F%2Fscipy.org%2F)
![GitLab Last Commit](https://img.shields.io/gitlab/last-commit/ByteMath%2Fpython%2FByMa?gitlab_url=https%3A%2F%2Fgitlab.com%2FByteMath%2Fpython%2FByMa&style=plastic)
![Static Badge](https://img.shields.io/badge/Docs-Read?style=plastic&label=Read&color=purple&link=https%3A%2F%2Fbytemath.gitlab.io%2Fpython%2FByMa%2Findex.html)



ByMaNiM is a Python package designed to facilitate the use of Manim video/slides. It is one of the major components of the ByMaNiM Slide Framework avialible on `npm` and `yarn`. 


## Installation

ByMaNiM is best installed in a [virtual environment](https://docs.python.org/3/library/venv.html).
We state the most common steps for creating and using a virtual environment here.
Refer to the documentation for more details.

To create a virtual environment run
```
python3 -m venv /path/to/new/virtual/environment
```

and to activate the virtual environment, run
```
source /path/to/new/virtual/environment/bin/activate
```

After this, we can install ByMaNiM from the pip package by using
```
pip install bymanim
```

In case the dependencies are not installed, you can run 
```
pip install -e .
```

## Packages

ByMaNiM consists of several subpackages, each serving a distinct purpose:

- **components**: Set of components for Manim Video and Slides
- **slide**: Set of pre-set Manim slides

## Authors

* Lorenzo Zambelli [website](https://lorenzozambelli.it)