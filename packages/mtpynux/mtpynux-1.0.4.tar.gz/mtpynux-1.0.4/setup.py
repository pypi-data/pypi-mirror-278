from setuptools import setup, find_packages

setup(
  name = 'mtpynux',
  packages = find_packages(include = ['mtpynux*']),
  version = '1.0.4',
  description = 'METATRADER PYTHON LINUX',
  long_description = open('README.txt', 'r').read(),
  long_description_content_type = 'text/markdown',
  author = 'Original By Lucas Prett Campagna',
  license = 'MIT',
  url = 'https://github.com/pythonsystem/mtpynux',
  install_requires = open('requirements.txt', 'r').read().split('\n'),
  setup_requires = [],
  tests_require = [],
)
