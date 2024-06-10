from setuptools import setup, find_packages

setup(
  name = 'mtnetbri',
  version = '1.0.2',
  description = 'mtnetbri',
  url = 'https://github.com/pythonsystem/mtnetbri',
  author = 'Lucas Campagna',
  license = 'MIT',
  long_description = open('README.txt', 'r').read(),
  long_description_content_type = 'text/plain',
  packages = find_packages(include = ['mtnetbri*']),
  install_requires = open('requirements.txt', 'r').read().split('\n'),
  setup_requires = [],
  tests_require = [],
)
