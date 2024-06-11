# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snyk_metrics', 'snyk_metrics.clients']

package_data = \
{'': ['*']}

install_requires = \
['datadog>=0.43.0,<1.0.0', 'prometheus-client>=0.12.0,<1.0.0']

setup_kwargs = {
    'name': 'snyk-metrics',
    'version': '0.0.6',
    'description': 'Python library to interact transparently with Prometheus, Pushgateway and Dogstatsd.',
    'long_description': '# snyk-python-metrics\n\nPython library to interact transparently with Prometheus, Pushgateway and\nDogstatsd.\n\n## Usage\n\nThe client can be used with two different approaches, one more opinionated and\nstructured, with all the metrics created and registered at the creation of the\nclient, and one more flexible, where metrics can be registered at any time.\n\nThe first approach should help keeping the application using this client cleaner\nand the metrics management in a centralised place.\n\n### Example 1 - "Locked Registry"\n\nIn this example all the metrics used by the application are registered as part\nof the client initialisation.\n\nExample:\n\n```python\n# my_app/settings.py\nfrom snyk_metrics import initialise, Counter\n\ncounter_1 = Counter(\n    name="my_app_counter",\n    documentation="Simple example counter",\n    label_names=None,\n)\ncounter_2 = Counter(\n    name="my_app_requests",\n    documentation="Requests per endpoint and method",\n    label_names=("endpoint", "method"),\n)\n\nmetrics = [counter_1, counter_2]\n\ninitialise(metrics=metrics, prometheus_enabled=True)\n```\n\n```python\n# my_app/api/endpoints.py\nfrom my_app.metrics import counter_1, counter_2\n\n\ndef my_function():\n    counter_1.increment()\n\n\ndef foo_get_endpoint():\n    counter_2.increment()\n```\n\n### Example 2 - "Unstructured flexibility"\n\nIn this example metrics are created and used within the same file. It could make\nit harder to keep track of all the metrics in the application, but it can also\nhelp in keeping them closer to the part of the project where the metrics are\nused.\n\n```python\n# my_app/settings.py\nfrom snyk_metrics import initialise\n\ninitialise(prometheus_enabled=True, lock_registry=False)\n```\n\n```python\n# my_app/api/endpoints.py\nfrom snyk_metrics import Counter\n\ncounter_1 = Counter(\n    name="my_app_counter",\n    documentation="Simple example counter",\n    label_names=None,\n)\ncounter_2 = Counter(\n    name="my_app_requests",\n    documentation="Requests per endpoint and method",\n    label_names=("endpoint", "method"),\n)\n\n\ndef my_function():\n    counter_1.increment()\n\n\ndef foo_get_endpoint():\n    counter_2.increment()\n```\n',
    'author': 'Snyk Security R&D',
    'author_email': 'security-engineering@snyk.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/snyk/python-metrics',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
