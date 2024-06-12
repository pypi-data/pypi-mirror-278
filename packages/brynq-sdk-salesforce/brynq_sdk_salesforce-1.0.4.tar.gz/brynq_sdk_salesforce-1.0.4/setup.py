from setuptools import setup


setup(
    name='brynq_sdk_salesforce',
    version='1.0.4',
    description='Salesforce wrapper from BrynQ',
    long_description='Salesforce wrapper from BrynQ',
    author='BrynQ',
    author_email='support@brynq.com',
    packages=["brynq_sdk.salesforce"],
    license='BrynQ License',
    install_requires=[
        'brynq-sdk-brynq>=1',
        'requests>=2,<=3',
        'pandas>=1,<3',
        'pyarrow>=10'
    ],
    zip_safe=False,
)