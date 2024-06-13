import glob
from shutil import rmtree

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


class CleanCommand(setuptools.Command):
    """ Custom clean command to tidy up the project root. """
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        rmtree('build', ignore_errors=True)
        rmtree('dist', ignore_errors=True)
        for file in glob.glob('*.egg-info'):
            rmtree(file)


class PrepublishCommand(setuptools.Command):
    """ Custom prepublish command. """
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        rmtree('build', ignore_errors=True)
        rmtree('dist', ignore_errors=True)
        for file in glob.glob('*.egg-info'):
            rmtree(file)


setuptools.setup(
    cmdclass={
        'clean': CleanCommand,
        'prepublish': PrepublishCommand,
    },
    name='grapheditdistance',
    version='0.1.1',
    url='https://github.com/jmgomezsoriano/graph-edit-distance',
    license='LGPL2',
    author='José Manuel Gómez Soriano',
    author_email='jmgomez.soriano@gmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    description='A edit distance edition based on graphs.',
    packages=setuptools.find_packages(exclude=["test"]),
    package_dir={'grapheditdistance': 'grapheditdistance'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        'networkx~=2.8.1',
        'matplotlib~=3.5.2',
        'numpy>=1.22,<1.27',
        'multivaluedbtree~=0.0.1',
        'mysmallutils~=1.0.18'
    ]
)
