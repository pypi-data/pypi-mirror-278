from setuptools import setup, find_packages
import codecs
import re
import os.path
here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    return codecs.open(os.path.join(here, *parts), 'r').read()


setup(
    name='prefect-test',
    version='0.0.1',
    description='Submission and monitoring of jobs and notebooks using the Yeedu API in prefect. ',
    long_description_content_type='text/markdown',
    author='pravallika',
    author_email='pravallika.akumuri@modak.com',
    packages=find_packages(),
   install_requires=[
    'prefect>=2.19.4',
    'requests>=2.27',
    'websocket-client>=1.8.0',
    'rel>=0.4.9.19',
    ],
    license='All Rights Reserved',
)

