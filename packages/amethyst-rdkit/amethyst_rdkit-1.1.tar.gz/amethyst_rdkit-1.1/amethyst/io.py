import os
import re
from dataclasses import dataclass
from typing import List, Optional, Union

from loguru import logger
from rdkit.Chem.AllChem import Mol, MolFromSmiles, MolToSmiles

from amethyst.utils import mols_to_str



@dataclass
class Substituents:
    """Dataclass used for storing a list of R-groups with their respective R#.

    Attributes:
        r_num (int): R#
        subs (List[Mol]): List of substituents in Mol object

    """

    r_num: int
    subs: List[Mol]


# NOTE - refactor regexes maybe?
def parse_file_input(
    filepath: str,
    r_num: Optional[int] = None,
    delimiter: Optional[str] = None,
    multiple_rs: Optional[bool] = False,
) -> List[Substituents]:
    """Parses provided file to a Substituents dataclass. Accepts R-groups marked as either isotope labels or atom maps. Newline separated file can only be for one R#.

    Args:
        filepath (str): Path to file with R-groups. Required.
        r_num (int): Number of R-group attached to the Substituents dataclass. Can be passed as R# (case insensitive) in a filename.
        delimiter (Optional[str], optional): Delimiter for one-line files. Defaults to newline.
        multiple_rs (Optional[bool], optional): Flag determining if each line in a file should be considered different R-group. First line is R1 and so on. Defaults to False.

    Raises:
        FileNotFoundError: Raised if supplied path isn't a file.
        ValueError: Raised if no r_num was provided.

    Returns:
        Substituents: Parsed file saved to dataclass.
    """
    if os.path.isfile(filepath):
        logger.debug("File path is good.")
        pass
    else:
        logger.error(f"{filepath} is not a file!")
        raise FileNotFoundError(f"{filepath} is not a file!")

    if r_num is None and not multiple_rs:
        path_split = re.split(r"(\\\\)|(/)|(\\)", filepath)
        m = re.match("[rR][0-9]+", path_split[-1])
        if m is not None:
            r_num = int(m.group(0))
        else:
            raise ValueError("R# is missing.")

    logger.debug(f"File given for R{r_num}.")

    subs_list: List[Mol] = []
    r = f"[*:{r_num}]"

    subs: List[Substituents] = []

    with open(filepath, "r") as file:
        if delimiter is None:
            for i in file:
                m = re.sub(r"\[[0-9]\*\]|\[.\:[0-9]\]", r, i)
                subs_list.append(MolFromSmiles(m))
                logger.debug(f"SMILES added: {m}")
            subs.append(Substituents(r_num, subs_list))
        else:
            lines: List[str] = file.readlines()
            logger.debug(lines)
            if multiple_rs:
                # TODO - Write tests
                for line in lines:
                    r = f"[*:{r_num}]"
                    m = re.sub(r"\[[0-9]\*\]|\[.\:[0-9]\]", r, line)
                    split_lines: List[str] = m.split(delimiter)
                    subs.append(
                        Substituents(r_num, [MolFromSmiles(x) for x in split_lines])
                    )
                    logger.debug(f"R{r_num} SMILES: {split_lines}")
                    r_num = r_num + 1
            else:
                for line in lines:
                    m = re.sub(r"\[[0-9]\*\]|\[.\:[0-9]\]", r, line)
                    split_lines: List[str] = m.split(delimiter)
                    subs.append(
                        Substituents(r_num, [MolFromSmiles(x) for x in split_lines])
                    )
                    logger.debug(f"SMILES added: {split_lines}")

    logger.debug(f"Final sub list: {mols_to_str(subs_list)}")

    return subs


def parse_mol_input(mols: List[List[Union[Mol, str]]]) -> List[Substituents]:
    """Parses list of molecules to a Substituents class. R# is handled via the list index (n+1) e.g., first list of Mol's in the list passed will have R1 number and so on.

    Args:
        mols (List[List[Mol]]): List containing another list of R-groups.

    Raises:
        ValueError: Raised when input isn't Mol or str.

    Returns:
        List[Substituents]: Returns subs parsed into a list of Substituents dataclass.
    """
    r_num = 1
    substituents_list = []
    for i in mols:
        if type(i[0]) is Mol:
            logger.debug("Mol input detected.")
            mols_smi = [MolToSmiles(x) for x in i]
        elif isinstance(i[0], str):
            logger.debug("String input detected.")
            mols_smi = mols[r_num - 1]
        else:
            raise ValueError("Wrong input type.")

        smis_relabelled = []
        for j in mols_smi:
            r = f"[*:{r_num}]"
            logger.debug(f"Inner: {j}")
            if isinstance(j, str):
                m = re.sub(r"\[[0-9]\*\]|\[\*\:[0-9]\]", r, j)
            elif type(j) is Mol:
                smi = MolToSmiles(j)
                m = re.sub(r"\[[0-9]\*\]|\[\*\:[0-9]\]", r, smi)
            else:
                raise ValueError("Wrong input type.")
            logger.debug(f"Relabelled SMILES: {m}")
            smis_relabelled.append(m)
            logger.debug(f"SMILES relabelled: {smis_relabelled}")

        mols_relabelled = [MolFromSmiles(x) for x in smis_relabelled]
        substituents_list.append(Substituents(r_num, mols_relabelled))
        logger.debug(f"R{r_num} SMILES: {mols_to_str(mols_relabelled)}")

        r_num = r_num + 1

    return substituents_list
