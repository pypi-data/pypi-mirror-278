from setuptools import setup, find_packages

setup(
    name="astronuts-python-reporter",
    version="0.0.2",
    packages=find_packages(),
    install_requires=[
        'pytest',
    ],
    entry_points={
        'console_scripts': [
            'astronuts-generate=src.main:main',
        ],
    },

    author="astronuts",
    description="A package to automate running pytest and transforming reports.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/astronuts-app/astronuts-python-reporter",
)
