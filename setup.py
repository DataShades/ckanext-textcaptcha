from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
    name='ckanext-textcaptcha',
    version=version,
    description="Text Captcha extension",
    long_description='''
    ''',
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='LinkDigital',
    url='',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.textcaptcha'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'ckanapi'
    ],
    entry_points='''
        [ckan.plugins]
        textcaptcha=ckanext.textcaptcha.plugin:TextCaptchaPlugin
    ''',
)
