# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['classy',
 'classy.features',
 'classy.index',
 'classy.sources',
 'classy.sources.cds',
 'classy.sources.pds',
 'classy.taxonomies',
 'classy.taxonomies.mahlke',
 'classy.utils']

package_data = \
{'': ['*'],
 'classy': ['data/*',
            'data/classy/*',
            'data/input/*',
            'data/mcfa/*',
            'data/mixnorm/*']}

install_requires = \
['aiohttp>=3.8',
 'click>=8.1.2',
 'importlib-resources>=5.10.2',
 'lmfit>=1.2.0',
 'matplotlib>=3.7.0',
 'mcfa>=0.1,<0.2',
 'numpy>=1.22.3',
 'pandas>=1.4.2',
 'rich>=12.2.0',
 'scikit-learn>=1.2.1',
 'space-rocks>=1.9.7']

entry_points = \
{'console_scripts': ['classy = classy.cli:cli_classy']}

setup_kwargs = {
    'name': 'space-classy',
    'version': '0.8.3',
    'description': 'classification tool for minor bodies using reflectance spectra and visual albedos',
    'long_description': '<p align="center">\n  <img width="260" src="https://raw.githubusercontent.com/maxmahlke/classy/master/docs/_static/logo_classy.svg">\n</p>\n\n<p align="center">\n  <a href="https://github.com/maxmahlke/classy#features"> Showcase </a> - <a href="https://github.com/maxmahlke/classy#install"> Install </a> - <a href="https://github.com/maxmahlke/classy#documentation"> Documentation </a>\n</p>\n\n<br>\n\n<div align="center">\n  <a href="https://img.shields.io/pypi/pyversions/space-classy">\n    <img src="https://img.shields.io/pypi/pyversions/space-classy"/>\n  </a>\n  <a href="https://img.shields.io/pypi/v/space-classy">\n    <img src="https://img.shields.io/pypi/v/space-classy"/>\n  </a>\n  <a href="https://readthedocs.org/projects/classy/badge/?version=latest">\n    <img src="https://readthedocs.org/projects/classy/badge/?version=latest"/>\n  </a>\n  <a href="https://arxiv.org/abs/2203.11229">\n    <img src="https://img.shields.io/badge/arXiv-2203.11229-f9f107.svg"/>\n  </a>\n</div>\n\n<br>\n\nA tool to explore, download, analyse, and classify asteroid reflectance\nspectra. Originally designed for classification in the taxonomy of [Mahlke,\nCarry, and Mattei 2022](https://arxiv.org/abs/2203.11229), it now offers\nmultiple taxonomic systems and a suite of quality-of-life features for\nspectroscopic analysis.\n\n# Showcase\n\nThings that ``classy`` tries to do well. All functionality is available via the command line and the `python` interface.\nSome functionality is available via the [web interface](https://classy.streamlit.app).\n\n**Explore and compare.**\n\nQuickly find and download spectra in public repositories.\n\n*Example*: List all spectra of asteroids in the Themis family with albedos up to 0.06 that cover the 0.45-1.8μm range.\n\n```shell\n$ classy spectra --wave_min 0.45 --wave_max 1.8 --family Themis --albedo ,0.06\n+-----------+--------+----------+----------+--------+---------------------+--------+--------+-----------------+\n| name      | number | wave_min | wave_max | phase  | date_obs            | family | albedo | shortbib        |\n+-----------+--------+----------+----------+--------+---------------------+--------+--------+-----------------+\n| Themis    | 24     | 0.435    | 2.49     | 12.917 | 2005-10-08T05:28:30 | Themis | 0.051  | MITHNEOS Unpub. |\n| Themis    | 24     | 0.45     | 2.4      | -      | -                   | Themis | 0.051  | Fornasier+ 2016 |\n| Themis    | 24     | 0.435    | 2.49     | 12.876 | 2005-10-08T00:00:00 | Themis | 0.051  | DeMeo+ 2009     |\n| Adorea    | 268    | 0.44     | 2.4      | -      | -                   | Themis | 0.039  | Fornasier+ 2016 |\n| Lipperta  | 846    | 0.45     | 2.39     | -      | -                   | Themis | 0.05   | Fornasier+ 2016 |\n| Lermontov | 2222   | 0.45     | 2.38     | -      | -                   | Themis | 0.051  | Fornasier+ 2016 |\n+-----------+--------+----------+----------+--------+---------------------+--------+--------+-----------------+\n                                                    6 Spectra\n```\n\n**Analyse and classify.**\n\nPersistent preprocessing and feature recognition for quick classification.\n\n*Example*: Classify the spectra above following Mahlke+ 2022, DeMeo+ 2009, and Tholen 1984.\n\n```shell\n$ classy classify --wave_min 0.45 --wave_max 1.8 --family Themis --albedo ,0.06\n+-----------+--------+----------+----------+--------+--------------+-------------+--------------+-----------------+\n| name      | number | wave_min | wave_max | albedo | class_mahlke | class_demeo | class_tholen | shortbib        |\n+-----------+--------+----------+----------+--------+--------------+-------------+--------------+-----------------+\n| Themis    | 24     | 0.435    | 2.490    | 0.0507 | C            | C           | G            | MITHNEOS Unpub. |\n| Themis    | 24     | 0.450    | 2.400    | 0.0507 | C            | C           |              | Fornasier+ 2016 |\n| Themis    | 24     | 0.435    | 2.490    | 0.0507 | C            | C           | G            | DeMeo+ 2009     |\n| Adorea    | 268    | 0.440    | 2.400    | 0.0389 | S            |             |              | Fornasier+ 2016 |\n| Lipperta  | 846    | 0.450    | 2.390    | 0.0504 | P            | X           |              | Fornasier+ 2016 |\n| Lermontov | 2222   | 0.450    | 2.380    | 0.0513 | P            | C           |              | Fornasier+ 2016 |\n+-----------+--------+----------+----------+--------+--------------+-------------+--------------+-----------------+\n                                                      6 Spectra\n```\n\n**Visualise and export.**\n\nQuick-look plots at any step to verify your analysis.\n\n*Example*: Show the spectra and the classification results.\n\n```shell\n$ classy classify --wave_min 0.45 --wave_max 1.8 --family Themis --albedo ,0.06 --plot\n```\n\n![Classified spectra](https://classy.readthedocs.io/en/latest/_images/spectra_classified_dark.png)\n\n# Install\n\n`classy` is available on the [python package index](https://pypi.org) as `space-classy`:\n\n``` sh\n$ pip install space-classy[gui]\n```\n\n# Documentation\n\nCheck out the documentation at [classy.readthedocs.io](https://classy.readthedocs.io/en/latest/) or run\n\n     $ classy docs\n',
    'author': 'Max Mahlke',
    'author_email': 'max.mahlke@oca.eu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/maxmahlke/classy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
