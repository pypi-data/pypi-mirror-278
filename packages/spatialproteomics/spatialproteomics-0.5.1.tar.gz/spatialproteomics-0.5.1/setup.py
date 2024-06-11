# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spatialproteomics',
 'spatialproteomics.la',
 'spatialproteomics.pl',
 'spatialproteomics.pp',
 'spatialproteomics.tl']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.3,<4.0.0',
 'scikit-image>=0.19.3,<0.20.0',
 'scikit-learn>=1.2.2,<2.0.0',
 'tqdm>=4.64.0,<5.0.0',
 'xarray>=2022.6.0,<2023.0.0',
 'zarr>=2.14.2,<3.0.0']

extras_require = \
{'docs': ['Sphinx==4.2.0',
          'sphinx-rtd-theme==1.0.0',
          'sphinxcontrib-napoleon==0.7',
          'nbsphinx==0.8.9']}

setup_kwargs = {
    'name': 'spatialproteomics',
    'version': '0.5.1',
    'description': 'spatialproteomics provides tools for the analysis of highly multiplexed immunofluorescence data',
    'long_description': '# spatialproteomics\n\n[![PyPI version](https://badge.fury.io/py/spatialproteomics.svg)](https://badge.fury.io/py/spatialproteomics)\n\n`spatialproteomics` is a light weight wrapper around `xarray` with the intention to facilitate the processing, exploration and analysis of highly multiplexed immunohistochemistry data.\n\n<p align="center" width="100%">\n    <img width="100%" src="docs/preview2.png">\n</p>\n\n## Principles\n\nMultiplexed imaging data comprises at least 3 dimensions (i.e. `channels`, `x`, and `y`) and has often additional data such as segmentation masks or cell type annotations associated with it. In `spatialproteomics`, we use `xarray` to create a data structure that keeps all of these data dimension in sync. This data structure can then be used to apply all sorts of operations to the data. Users can segment cells, perform different image processing steps, quantify protein expression, predict cell types, and plot their data in various ways. By providing researchers with those tools, `spatialproteomics` can be used to quickly explore highly multiplexed spatial proteomics data directly within jupyter notebooks.\n\n\n## Installation\n\nTo install `spatialproteomics` first create a python environment and install the package using \n\n```\npip install spatialproteomics\n```\n\nCheck the documentation for further information https://sagar87.github.io/spatialproteomics/.\n',
    'author': 'Harald Vohringer',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
