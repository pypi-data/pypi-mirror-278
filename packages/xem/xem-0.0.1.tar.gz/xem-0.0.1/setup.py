#!/usr/bin/env python

from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(name='xem',
      version='0.0.1',
      description=('A lightweight self-hosted web analytics '
                   'server written in Flask and python.'),
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Huy Nguyen',
      author_email='121183+huyng@users.noreply.github.com',
      packages=['xem', "xem.templates"],
      package_data={
          'xem.templates': ['*.html']
      },
      install_requires=["Flask", "gunicorn"],
      zip_safe=False,
      url="https://github.com/huyng/xem")

# to distribute run:
# python setup.py register sdist upload
# python -m twine  upload dist
