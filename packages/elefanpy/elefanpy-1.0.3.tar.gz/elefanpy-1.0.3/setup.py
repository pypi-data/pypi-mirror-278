from setuptools import setup, find_packages

setup(
  name = 'elefanpy',
  version = '1.0.3',
  description = 'elefanpy',
  url = 'https://github.com/pythonsystem/elefanpy',
  author = 'Open Liberal',
  license = 'MIT',
  long_description = open('README.txt', 'r').read(),
  long_description_content_type = 'text/plain',
  packages = find_packages(include = ['elefanpy*']),
  install_requires = open('requirements.txt', 'r').read().split('\n'),
  setup_requires = [],
  tests_require = [],
)
