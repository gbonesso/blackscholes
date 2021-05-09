import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.1.0'
PACKAGE_NAME = 'blackscholes'
AUTHOR = 'Gustavo Bonesso'
AUTHOR_EMAIL = 'gustavo_bonesso@hotmail.com'
URL = 'https://github.com/gbonesso/blackscholes'

LICENSE = 'MIT License'
DESCRIPTION = 'This is a Python lib implementing Black and Scholes formulas'
#LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESCRIPTION = 'This is a Python lib implementing Black and Scholes formulas'
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
      'numpy',
      'pandas'#,
      #'os',
      #'zipfile',
      #'logging'
]

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages()
      )