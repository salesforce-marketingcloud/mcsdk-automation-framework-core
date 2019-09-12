from setuptools import setup

setup(
    name='mcsdk-automation-framework-core',
    version='1.0.0',
    package_dir={'': 'src'},
    packages=[
        'mcsdk',
        'mcsdk.git',
        'mcsdk.integration',
        'mcsdk.integration.os'
    ],
    url='https://github.com/salesforce-marketingcloud/MCSDK-Automation-Framework-Core',
    license='',
    author='sfadincescu',
    author_email='adincescu@salesforce.com',
    description='The library handles part of the CI process'
)
