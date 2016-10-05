#!/usr/bin/env python

from setuptools import setup, find_packages
from elks.__init__ import __version__

setup(name='elks',
      version=__version__,
      description='Tool for interacting with the 46elks API',
      url="https://github.com/46elks/elks",
      author="Emil Tullstedt",
      author_email='emil@46elks.com',
      license='MIT',
      packages = find_packages(),
      install_requires = ['requests>=2.10.0',
            'elkme>=0.4.5',
            'phonenumbers>=7.5.1',
            'Jinja2>=2.8',
            'MarkupSafe>=0.23'],
      tests_require = ['nose>=1.3.7'],
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: System :: Monitoring'
      ],
      keywords="sms 46elks monitoring",
      entry_points={
            'console_scripts': [
                'elks = elks:run'
                ]
          },
      use_2to3 = False,
      test_suite = 'nose.collector')

