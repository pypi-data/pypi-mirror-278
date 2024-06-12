import warnings

import MDAnalysis as mda

from .name_maps import Cterm_mod, Nterm_mod, res_mod, universal_mod

warnings.filterwarnings("ignore")


def transform_self_defined_dict(
    input_pdb_path,
    output_pdb_path,
    self_defined_dict: dict,
):
    """
    Transform the atom names in the input pdb file (ligand) based on the user-defined dictionary.

    Input:
        - `input_pdb_path`: str, the path to the input pdb file.
        - `self_defined_dict`: dict, the user-defined dictionary for renaming atoms.
        For example:
            self_defined_dict = {
                "B12": {
                    "H1P1": "H66",
                    "H1P2": "H67",
                    "H201": "H20A",
                    "H202": "H20B",
                }
                # resiude name: {old atom name: new atom name}
            }
    Output:
        - `output_pdb_path`: str, the path to the output pdb file.
    """
    u = mda.Universe(input_pdb_path)
    for residue in u.residues:
        tmp = []
        for name in residue.atoms.names:
            if name in self_defined_dict.keys():
                tmp.append(self_defined_dict[name])
            else:
                tmp.append(name)
        residue.atoms.names = tmp
    u.select_atoms("all").write(output_pdb_path)


def transform_with_resname(
    input_pdb_path,
    output_pdb_path,
    residue_shift: int = 0,
):
    """
    Transform the atom names in the input pdb file (solutable protein) based on the residue-atom dictionary.

    Input:
        - `input_pdb_path`: str, the path to the input pdb file.
        - `residue_shift` (optional): int, the shift of residue number, default = 0.
        For example, 8hsc, since Modeller renumbered it to starting from resid 1, here we modified it back to start at resid 32.
    Output:
        - `output_pdb_path`: str, the path to the output pdb file.

    """
    # Load the pdb file
    u = mda.Universe(input_pdb_path)

    # Modify the resid
    # For example, 8hsc, since Modeller renumbered it to starting from resid 1,
    # we can modify it back to start at resid 32
    u.residues.resids = u.residues.resids + residue_shift

    # Select protein atoms, and get the resid of Nterm and Cterm
    u_p = u.select_atoms("protein")
    if len(u_p.residues) == 0:
        print("No protein atoms found in the input pdb file.")
        print("Termini residues are set to None.")
        Nterm_resid = None
        Cterm_resid = None
    else:
        Nterm_resid = u_p.residues.resids[0]
        Cterm_resid = u_p.residues.resids[-1]

    # Rename atoms based on the residue-atom dictionary
    for residue in u.residues:
        tmp = []
        for name in residue.atoms.names:
            # if residue.resname in res_mod.keys():
            #     if name in res_mod[residue.resname].keys():
            #         tmp.append(res_mod[residue.resname][name])
            if name in universal_mod.keys():
                tmp.append(universal_mod[name])
            elif name in Nterm_mod.keys() and residue.resid == Nterm_resid:
                tmp.append(Nterm_mod[name])
            elif name in Cterm_mod.keys() and residue.resid == Cterm_resid:
                tmp.append(Cterm_mod[name])
            elif (
                residue.resname in res_mod.keys()
                and name in res_mod[residue.resname].keys()
            ):
                tmp.append(res_mod[residue.resname][name])
            else:
                tmp.append(name)
        residue.atoms.names = tmp

    # Rename residue name for histidine
    for residue in u.residues:
        if residue.resname == "HIS":
            if "HD1" in residue.atoms.names and "HE2" in residue.atoms.names:
                residue.resname = "HSP"
            elif "HD1" in residue.atoms.names and "HE2" not in residue.atoms.names:
                residue.resname = "HSD"
            elif "HD1" not in residue.atoms.names and "HE2" in residue.atoms.names:
                residue.resname = "HSE"
    u.select_atoms("all").write(output_pdb_path)


def transform_resname(
    input_pdb_path,
    output_pdb_path,
    from_resname: str,
    to_resname: str,
):
    """
    Transform the residue name in the input pdb file.

    Input:
        - `input_pdb_path`: str, the path to the input pdb file.
        - `from_resname`: str, the residue name to be changed.
        - `to_resname`: str, the new residue name.

    Output:
        - `output_pdb_path`: str, the path to the output pdb file.
    """
    # Load the pdb file
    u = mda.Universe(input_pdb_path)

    # Rename residue name
    for residue in u.residues:
        if residue.resname == from_resname:
            residue.resname = to_resname

    u.select_atoms("all").write(output_pdb_path)
