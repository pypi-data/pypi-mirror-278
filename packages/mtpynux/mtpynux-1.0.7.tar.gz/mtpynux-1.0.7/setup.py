from setuptools import setup, find_packages

setup(
  name = 'mtpynux',
  version = '1.0.7',
  description = 'METATRADER PYTHON LINUX',
  url = 'https://github.com/pythonsystem/mtpynux',
  author = 'Original By Lucas Campagna',
  license = 'MIT',
  long_description = open('README.txt', 'r').read(),
  long_description_content_type = 'text/plain',
  packages = find_packages(include = ['mtpynux*']),
  install_requires = open('requirements.txt', 'r').read().split('\n'),
  setup_requires = [],
  tests_require = [],
)
