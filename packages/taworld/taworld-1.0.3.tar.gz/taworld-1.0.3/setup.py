from setuptools import setup, find_packages

setup(
  name = 'taworld',
  version = '1.0.3',
  description = 'TECHNICAL ANALYSIS WORLD',
  url = 'https://github.com/pythonsystem/taworld',
  author = 'Original By Kevin Johnson',
  license = 'MIT',
  long_description = open('README.txt', 'r').read(),
  long_description_content_type = 'text/plain',
  packages = find_packages(include = ['taworld*']),
  install_requires = open('requirements.txt', 'r').read().split('\n'),
  setup_requires = [],
  tests_require = [],
)
