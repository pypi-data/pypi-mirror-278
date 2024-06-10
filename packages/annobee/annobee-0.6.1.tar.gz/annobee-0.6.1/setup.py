from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    description = fh.read()


setup(
    name='annobee',
    version='0.6.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'annobee=annobee.cli:main',
        ],
    },
    install_requires=[
        'numpy',
        'pandas',
        'tqdm',
        'dnspython',
        'pymongo',
        'requests',
        'six',
        'tzdata',
        'python-dateutil',
        'pytz',
        'pool',
    ],
    include_package_data=True,
    url='https://github.com/variantAnnotation/annobee-sdk',  # Update with your repository URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    long_description=description,
    long_description_content_type="text/markdown",
    python_requires='>=3.6',
)
