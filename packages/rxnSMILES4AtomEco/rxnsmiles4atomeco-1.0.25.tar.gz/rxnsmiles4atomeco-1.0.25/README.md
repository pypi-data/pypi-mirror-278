
# rxnSMILES4AtomEco:

    This package provides functions to calculate the atom economy of chemical reactions using reaction SMILES.
    It utilizes the RDKit library to handle molecular structures and properties.

### Features:
    - Calculation of atom economy for reactions
    - Handling of multiple reactions in a single calculation
    - Support for different types of reaction SMILES
    - Programmatic output of atom economy numerical value
    
### Usage:
    To use the package, simply import the relevant functions and provide reaction SMILES as input.
    
### Example:
    
    from rxnSMILES4AtomEco import calculate_atom_economy
    
    reactions_smiles = "C.O>catalyst>{3}[HH]"
    
    calculate_atom_economy(reactions_smiles)
    
    For more information, please refer to the documentation at https://pypi.org/project/rxnSMILES4AtomEco/