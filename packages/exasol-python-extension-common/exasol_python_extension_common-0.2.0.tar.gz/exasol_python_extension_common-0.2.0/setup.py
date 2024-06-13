# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['exasol',
 'exasol.python_extension_common',
 'exasol.python_extension_common.deployment']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.7,<9.0.0',
 'exasol-bucketfs>=0.10.0',
 'exasol-saas-api>=0.7.0,<1.0.0',
 'pyexasol>=0.25.0,<0.26.0',
 'requests<2.32.0',
 'tenacity>=8.3.0,<9.0.0']

setup_kwargs = {
    'name': 'exasol-python-extension-common',
    'version': '0.2.0',
    'description': 'A collection of common utilities for Exasol extensions.',
    'long_description': '# Exasol Python Extension Common\n\nA package with common functionality, shared by Exasol Python Extensions, e.g.\n* [transformers-extension](https://github.com/exasol/transformers-extension)\n* [sagemaker-extension](https://github.com/exasol/sagemaker-extension)\n\n## Features\n\nA deployer for script language containers (SLC) to be used by UDF-based extensions of Exasol database requiring a special SLC.\n\n## More documentation\n\n* User Guide\n* [Developer Guide](doc/developer-guide.md)\n* [User Defined Functions (UDF)](https://docs.exasol.com/db/latest/database_concepts/udf_scripts.htm)\n* [Script Language Containers (SLC)](https://github.com/exasol/script-languages-release/)\n',
    'author': 'Mikhail Beck',
    'author_email': 'mikhail.beck@exasol.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<4.0',
}


setup(**setup_kwargs)
