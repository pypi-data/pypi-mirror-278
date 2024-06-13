from setuptools import setup, find_packages


setup (
    name ="SIWP2005-Kenlie-sort",
    version = "0.0.1",
    author = "Kenlie Athalla Bintang",
    author_email = "kenlie.422023024@civitas.ukrida.ac.id",
    description = "A package that provides implementations of various sorting algorithms.",
    long_description =open('README.md').read(),
    long_description_content_type = "text/markdown",
    url ="",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
        )