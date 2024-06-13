from typing import List, Union

from rdkit.Chem.Draw import rdMolDraw2D
from rdkit.Chem.rdchem import Atom, Mol
from rdkit.Chem.rdmolfiles import MolFromSmiles, MolToSmiles


# Checks whether passed SMILES string is a molecule or an atom
# Works although a bit hacky
# Should this go to io.py?
def mol_or_atom(smiles: str) -> Union[Mol, Atom]:
    try:
        a = Atom(smiles)
        return a
    except Exception as e:
        return MolFromSmiles(smiles)


# Returns an image of molecule with atom idx's
def depict_mol(mol: Mol, filename: str = "", size=(1000, 1000)):
    if filename == "":
        filename = MolToSmiles(mol)

    d = rdMolDraw2D.MolDraw2DCairo(size[0], size[1])

    d.drawOptions().addAtomIndices = True
    d.drawOptions().addAtomLabels = True
    d.DrawMolecule(mol)
    d.FinishDrawing()
    d.WriteDrawingText(f"png/{filename}.png")


def mols_to_str(mols: List[Mol]):
    return [MolToSmiles(x) for x in mols]