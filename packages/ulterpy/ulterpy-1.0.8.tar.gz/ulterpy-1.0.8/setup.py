from setuptools import setup, find_packages

setup(
  name = 'ulterpy',
  version = '1.0.8',
  description = 'ULTRA ERGONOMIC PYTHON',
  url = 'https://github.com/pythonsystem/ulterpy',
  author = 'Original By Open Liberal',
  license = 'MIT',
  long_description = open('README.txt', 'r').read(),
  long_description_content_type = 'text/plain',
  packages = find_packages(include = ['ulterpy*']),
  install_requires = open('requirements.txt', 'r').read().split('\n'),
  setup_requires = [],
  tests_require = [],
)
