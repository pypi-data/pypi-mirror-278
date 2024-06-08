from setuptools import setup, find_packages

setup(
  name = 'ulterpy',
  packages = find_packages(include = ['ulterpy*']),
  version = '1.0.5',
  description = 'ULTRA ERGONOMIC PYTHON',
  long_description = open('README.txt', 'r').read(),
  long_description_content_type = 'text/markdown',
  author = 'Original By Python Package Index',
  license = 'MIT',
  url = 'https://github.com/pythonsystem/ulterpy',
  install_requires = open('requirements.txt', 'r').read().split('\n'),
  setup_requires = [],
  tests_require = [],
)
