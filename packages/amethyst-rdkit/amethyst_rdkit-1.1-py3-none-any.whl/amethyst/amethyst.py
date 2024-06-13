from typing import List, Optional, Union

from loguru import logger
from rdkit.Chem.AllChem import Mol, MolFromSmiles, MolToSmiles
from rdkit.Chem.rdRGroupDecomposition import RelabelMappedDummies, RGroupLabelling
from rdkit.Chem.EnumerateStereoisomers import (
    EnumerateStereoisomers,
    StereoEnumerationOptions,
)

from amethyst.io import (
    Substituents,
    parse_file_input,
    parse_mol_input,
)
from amethyst.substitution import general_sub
from amethyst.utils import mols_to_str

logger.add("amethyst.log", level=10)


def enumerate(
    core: Union[str, Mol],
    r_num: Optional[int] = None,
    multiple_rs: bool = False,
    subs_path: Optional[str] = None,
    delimiter: Optional[str] = None,
    subs_mol: Optional[List[List[Union[Mol, str]]]] = None,
    enantiomers: bool = False,
    output_smi: bool = False,
) -> List[Union[Mol, str]]:
    """Enumerates scaffold molecule with provided R-groups. Can generate enantiomers.

    Args:
        core (Union[str, Mol]): Scaffold molecule
        r_num (int): R#.
        multiple_rs (bool): Flag determining if each line in a file should be considered different R-group. First line is R1 and so on. Defaults to False.
        subs_path (Optional[str], optional): Path to file with R-groups. Defaults to None.
        delimiter (Optional[str], optional): Delimiter used in provided file, can be any valid string. Defaults to newline.
        subs_mol (Optional[List[List[Union[Mol, str]]]], optional): R-groups provided in form of RDKit molecules. Defaults to None.
        enantiomers (bool, optional):  Flag determining generation of enantiomers after the enumeration. Defaults to False
        output_smi (bool, optional): Flag if output should be in SMILES or Mol objects. Defaults to False.

    Raises:
        ValueError: Raised either when both sources of molecules were given or none of them.

    Returns:
        List[Mol]: List of enumerated molecules.
    """
    if subs_path is not None and subs_mol is not None:
        logger.error("Both sources for R-groups passed")
        raise ValueError("Only one source of R-groups must be passed")
    elif subs_path is not None:
        logger.debug("Filepath passed")
        if r_num is not None:
            r_groups: List[Substituents] = parse_file_input(subs_path, r_num, delimiter)
        elif multiple_rs:
            r_groups: List[Substituents] = parse_file_input(subs_path, delimiter=delimiter, multiple_rs=True)
        else:
            raise ValueError("Either pass r_num or set multiple_rs to True")
    elif subs_mol is not None:
        logger.debug("Mol list passed")
        r_groups: List[Substituents] = parse_mol_input(subs_mol)
        [logger.debug(f"Parsed R-Groups: {mols_to_str(x.subs)}") for x in r_groups]
    else:
        logger.error("No R-groups were passed")
        raise ValueError("No R-groups passed!")

    if type(core) is not Mol:
        core = MolFromSmiles(core)
    
    RelabelMappedDummies(core, outputLabels=RGroupLabelling.AtomMap)

    analogues: List[Mol] = general_sub(core, r_groups)

    if enantiomers:
        params = StereoEnumerationOptions(tryEmbedding=True, unique=True)
        stereoisomers = [EnumerateStereoisomers(x, options=params) for x in analogues]
        if output_smi:
            return [MolToSmiles(x) for x in stereoisomers]
        else:
            return stereoisomers

    if output_smi:
        return [MolToSmiles(x) for x in analogues]
    else:
        return analogues
