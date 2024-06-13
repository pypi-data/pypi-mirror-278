# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['captureflow']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=2.0.30,<3.0.0',
 'opentelemetry-api>=1.25.0,<2.0.0',
 'opentelemetry-exporter-otlp>=1.25.0,<2.0.0',
 'opentelemetry-instrumentation-dbapi>=0.46b0,<0.47',
 'opentelemetry-instrumentation-fastapi>=0.46b0,<0.47',
 'opentelemetry-instrumentation-flask>=0.46b0,<0.47',
 'opentelemetry-instrumentation-httpx>=0.46b0,<0.47',
 'opentelemetry-instrumentation-requests>=0.46b0,<0.47',
 'opentelemetry-instrumentation-sqlalchemy>=0.46b0,<0.47',
 'opentelemetry-instrumentation-sqlite3>=0.46b0,<0.47',
 'opentelemetry-instrumentation>=0.46b0,<0.47',
 'opentelemetry-sdk>=1.25.0,<2.0.0',
 'python-dotenv==1.0.1',
 'wrapt>=1.16.0,<2.0.0']

entry_points = \
{'opentelemetry_distro': ['distro = captureflow.distro:CaptureFlowDistro']}

setup_kwargs = {
    'name': 'captureflow-agent',
    'version': '0.0.10',
    'description': 'The CaptureFlow Tracer is a Python package crafted for in-depth tracing of function calls within Python applications. Its primary function is to capture and relay execution data to the CaptureFlow server-side system for decision making.',
    'long_description': "# What\n\nOpenTelemetry-based tracer with custom instrumentations that are crucial for CaptureFlow.\n\n# Development\n\n- Uses Poetry, as it's easy to publish this way.\n\n# Running\n\nRun Jaeger-UI and trace collector via `docker-compose up`.\nRun your app via `opentelemetry-instrument uvicorn server:app`\n\nCheck your `http://localhost:16686/search` for application monitoring.",
    'author': 'Nick Kutz',
    'author_email': 'me@nikitakuts.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
