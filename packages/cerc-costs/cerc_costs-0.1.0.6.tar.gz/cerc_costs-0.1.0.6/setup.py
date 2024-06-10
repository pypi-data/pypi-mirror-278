import glob
import pathlib
from distutils.util import convert_path
from setuptools import setup

with pathlib.Path('requirements.txt').open() as r:
  install_requires = [
    str(requirement).replace('\n', '')
    for requirement
    in r.readlines()
  ]
install_requires.append('setuptools')

main_ns = {}
version = convert_path('costs/version.py')
with open(version) as f:
  exec(f.read(), main_ns)

setup(
  name='cerc-costs',
  version=main_ns['__version__'],
  description="CERC costs contains the basic cost calculation per CERC-Hub building",
  long_description="CERC costs contains the basic cost calculation per CERC-Hub building",
  classifiers=[
    "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
  ],
  include_package_data=True,
  packages=['costs'],
  setup_requires=install_requires,
  install_requires=install_requires,
  data_files=[
    ('costs', glob.glob('requirements.txt'))
  ]
)
