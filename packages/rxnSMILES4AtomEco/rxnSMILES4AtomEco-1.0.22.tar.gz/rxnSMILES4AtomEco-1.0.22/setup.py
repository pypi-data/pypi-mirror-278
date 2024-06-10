from setuptools import setup, find_packages

setup(
    name='rxnSMILES4AtomEco',
    version='1.0.22',
    packages=find_packages(),
    description='Calculate atom economy for chemical reactions using reaction SMILES',
    long_description='''\
    This package provides functions to calculate the atom economy of chemical reactions using reaction SMILES.
    It utilizes the RDKit library to handle molecular structures and properties.
    
    Features:
    - Calculation of atom economy for reactions
    - Handling of multiple reactions in a single calculation
    - Support for different types of reaction SMILES
    - Programmatic output of atom economy numerical value
    
    Usage:
    To use the package, simply import the relevant functions and provide reaction SMILES as input.
    
    Example:
    
    from rxnSMILES4AtomEco import calculate_atom_economy
    
    reactions_smiles = "C(CO)O.CCO.CC(C)O>CCO>C(C)O.CCO"
    
    calculate_atom_economy(reactions_smiles)
    
    For more information, please refer to the documentation at https://github.com/yourusername/rxnSMILES4AtomEco.
    ''',
    author='Samuele Giani',
    author_email='samuele.giani@empa.ch',
    url='https://pypi.org/project/rxnSMILES4AtomEco/',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
        python_requires='>=3.6',
    install_requires=[
        'rdkit',  # Add other dependencies here
    ],
)
