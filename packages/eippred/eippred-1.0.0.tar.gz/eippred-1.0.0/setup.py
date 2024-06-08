# setup.py

from setuptools import setup, find_packages
from setuptools import setup, Extension
from setuptools import  find_namespace_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
    name='eippred',
    version='1.0.0',
    description='EIPPred: A tool for predicting, designing, and scanning MIC of the  peptides',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license_files = ('LICENSE.txt',),
    author='Nisha Bajiya',
    author_email='nishab@iiitd.ac.in',
    url='https://github.com/raghavalab/eippred',
    packages=find_namespace_packages(where="src"),
    package_dir={'':'src'},
    package_data={'eippred.blast_binaries':['**/*'],
                  'eippred.Data':['**/*']},
    entry_points={'console_scripts' : ['eippred = eippred.python_scripts.eippred:main']},
    include_package_data=True,
    python_requires='>=3.6',
    install_requires= [ 'numpy', 'pandas', 'scikit-learn', 'argparse' ,'tqdm' ]
)

