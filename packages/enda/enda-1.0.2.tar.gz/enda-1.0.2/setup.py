# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['enda', 'enda.feature_engineering', 'enda.ml_backends', 'enda.tools']

package_data = \
{'': ['*']}

install_requires = \
['datatable>=1.1.0,<2.0.0',
 'h2o>=3.36.1.1,<4.0.0.0',
 'jours-feries-france>=0.7.0,<0.8.0',
 'numpy>=1.18,<2.0',
 'pandas>=1.4.0,<2.0.0',
 'polars>=0.20.0,<0.21.0',
 'scikit-learn>=1.0.2,<2.0.0',
 'statsmodels<=0.13.5',
 'unidecode>=1.3.4,<2.0.0',
 'vacances-scolaires-france>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'enda',
    'version': '1.0.2',
    'description': 'Tools to manipulate energy time-series and contracts, and to perform forecasts.',
    'long_description': "# enda\n\n![PyPI](https://img.shields.io/pypi/v/enda) [![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/) [![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)\n\n## What is it?\n\n**enda** is a Python package that provides tools to manipulate **timeseries** data in conjunction with **contracts** data for analysis and **forecasting**.\n\nInitially, it has been developed to help [Rescoop.eu](https://www.rescoop.eu/) members build various applications, such as short-term electricity load and production forecasts, specifically for the [RescoopVPP](https://www.rescoopvpp.eu/) project. Hence some tools in this package perform TSO (transmission network operator) and DNO (distribution network operator) data wrangling as well as weather data management. enda is mainly developed by [Enercoop](https://www.enercoop.fr/).\n\n## Main Features\n\nHere are some things **enda** does well:\n\n- Provide robust machine learning algorithms for **short-term electricity load and production forecasts**. enda provides a convenient wrapper around the popular multipurpose machine-learning backends [Scikit](https://scikit-learn.org/stable/) and [H2O](https://h2o.ai/platform/ai-cloud/make/h2o/). The load forecast was originally based on Komi Nagbe's thesis (<http://www.theses.fr/s148364>).\n- Manipulate **timeseries** data, such as load curves. enda handles timeseries-specific detection of missing data, like time gaps, frequency changes, extra values, as well as various resampling methods. \n- Provide several **backtesting** and **scoring** methods to ensure the quality of the trained algorithm on almost real conditions.\n- Manipulate **contracts** data coming from your ERP and turn it into timeseries you can use for analysis, visualisation and machine learning.\n- Date-time **feature engineering** robust to timezone hazards.\n\n## Where to get it\n\nThe source code is currently hosted on GitHub at: <https://github.com/enercoop/enda>. If you wish to run the examples it contains, you can clone enda from the Github repository\n\nBinary installers for the latest released version are available at the [Python\nPackage Index (PyPI)](https://pypi.org/project/enda) (for now it is not directly on [Conda](https://docs.conda.io/en/latest/)). \n\n\n```sh\npip install enda\n```\n\nor using [poetry](https://python-poetry.org/):\n\n```sh\npoetry add enda\n```\n\n## Documentation and API\n\nThe complete API is available online [here](https://enercoop.github.io/enda).\n\n\n## How to get started?\n\nFor a more comprehensive approach to enda, several [Jupyter notebooks](https://jupyter.org/) have been proposed in the [guides](<https://github.com/enercoop/enda/tree/main/guides>.).\nSome dependencies are needed to run these examples, that you can easily install with poetry, running ```poetry install enda[examples]```\n\n\n## Dependencies\n\n### Hard dependencies\n\n- [Pandas](https://pandas.pydata.org/)\n- [Scikit-learn](https://scikit-learn.org/stable/)\n- [H2O](https://docs.h2o.ai/)\n- [Numpy](https://numpy.org/)\n- [Statsmodels](https://pypi.org/project/statsmodels/)\n- Libraries that are recommended by the previous packages: [datatable](https://pypi.org/project/datatable/), [polars](https://pypi.org/project/polars/), [numexpr](https://pypi.org/project/numexpr/), [unidecode](https://pypi.org/project/Unidecode/)\n- Libraries meant to get calendar data: [jours-feries-france](https://pypi.org/project/jours-feries-france/), [vacances-scolaires-france](https://pypi.org/project/vacances-scolaires-france/)\n\n\n### Optional dependencies\n\nIf you want to run the examples, you may need extra dependencies. \nThese dependencies can be installed using poetry: \n\n```sh\npoetry install --with examples\n```\n\nor manually:\n\n```sh\npip install numexpr bottleneck pandas enda jupyter h2o scikit-learn statsmodels joblib matplotlib\n```\n\nAccordingly, if you wish to develop into enda, we suggest some tools and linters that can be used. \n```sh\npoetry install --with dev\n```\n\n## License\n\n[MIT](LICENSE)\n",
    'author': 'Enercoop',
    'author_email': 'team-data@enercoop.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/enercoop/enda',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.0,<4.0.0',
}


setup(**setup_kwargs)
