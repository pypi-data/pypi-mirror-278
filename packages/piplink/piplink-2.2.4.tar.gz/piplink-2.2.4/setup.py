from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='piplink',
    version='2.2.4',
    author='Fidal',
    author_email='mrfidal@proton.me',
    url='https://mrfidal.in/basic-pip-package/piplink',
    description='A simple package for uploading packages to PyPI',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'requests',
        'requests-toolbelt',
    ],
    entry_points={
        'console_scripts': [
            'piplink=piplink.upload:main',
        ],
    },
)
