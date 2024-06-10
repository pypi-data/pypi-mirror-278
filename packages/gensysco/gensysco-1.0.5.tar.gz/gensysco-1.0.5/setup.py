from setuptools import setup, find_packages

setup(
  name = 'gensysco',
  version = '1.0.5',
  description = 'gensysco',
  url = 'https://github.com/pythonsystem/gensysco',
  author = 'Digital Community',
  license = 'MIT',
  long_description = open('README.txt', 'r').read(),
  long_description_content_type = 'text/plain',
  packages = find_packages(include = ['gensysco*']),
  install_requires = open('requirements.txt', 'r').read().split('\n'),
  setup_requires = [],
  tests_require = [],
)
