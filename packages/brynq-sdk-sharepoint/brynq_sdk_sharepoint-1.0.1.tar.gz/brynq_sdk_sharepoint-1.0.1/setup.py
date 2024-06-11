from setuptools import setup


setup(
    name='brynq_sdk_sharepoint',
    version='1.0.1',
    description='Sharepoint wrapper from BrynQ',
    long_description='Sharepoint wrapper from BrynQ',
    author='BrynQ',
    author_email='support@brynq.com',
    packages=["brynq_sdk.sharepoint"],
    license='BrynQ License',
    install_requires=[
        'brynq-sdk-brynq>=1',
        'requests>=2,<=3'
    ],
    zip_safe=False,
)