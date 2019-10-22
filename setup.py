from setuptools import setup

setup(
    name='mcsdk-automation-framework-core',
    version='0.0.0',
    package_dir={'': 'src'},
    packages=[
        'mcsdk',
        'mcsdk.git',
        'mcsdk.integration',
        'mcsdk.integration.os',
        'mcsdk.codebase'
    ],
    url='https://github.com/salesforce-marketingcloud/mcsdk-automation-framework-core',
    license='',
    author='salesforce-marketingcloud',
    author_email='splumlee@salesforce.com',
    description='The library handles part of the CI process'
)
