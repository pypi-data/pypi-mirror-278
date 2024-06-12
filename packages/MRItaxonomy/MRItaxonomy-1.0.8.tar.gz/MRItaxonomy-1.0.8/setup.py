from setuptools import setup, find_packages

setup(
    name="MRItaxonomy",
    version="1.0.8",
    packages=find_packages(),
    install_requires=['pandas>=0.19.0',
                      'biopython>=1.7',
                      'wget>=3.2',
                      'marisa_trie>=1.1.0'],
    author="MRIGlobal Bioinformatics Team",
    author_email="biofx@mriglobal.org",
    keywords="mriglobal taxonomy ncbi",
    description="MRIGlobal's taxonomy related operators",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT", # or the license you chose
    url="https://github.com/mriglobal/MRItaxonomy",
    classifiers=[
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
    ],
)
