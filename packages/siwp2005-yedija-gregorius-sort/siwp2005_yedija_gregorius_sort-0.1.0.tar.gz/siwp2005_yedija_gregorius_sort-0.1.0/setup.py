from setuptools import setup, find_packages

setup(
    name="siwp2005-yedija_gregorius-sort",
    version="0.1.0",
    author="Yedija Gregorius",
    author_email="yedija.422023007@civitas.ukrida.ac.id",
    description="A package that provides implementations of various sorting algorithms.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/yourusername/siwp2005-name-sort",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
