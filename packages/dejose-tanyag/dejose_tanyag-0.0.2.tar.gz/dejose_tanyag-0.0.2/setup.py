from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name='dejose_tanyag',
    version='0.0.2',
    packages=find_packages(),
    description='Simple Library',
    author='Tanyag & De Jose',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    long_description=description,
    long_description_content_type='text/markdown',
)