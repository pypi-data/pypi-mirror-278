import warnings

import MDAnalysis as mda

from .name_maps import Cterm_mod, Nterm_mod, res_mod, universal_mod

warnings.filterwarnings("ignore")


def transform_with_resname(input_pdb_path, output_pdb_path, residue_shift: int = 0):
    u = mda.Universe(input_pdb_path)
    u.residues.resids = u.residues.resids + residue_shift
    # For example, 8hsc, since Modeller renumbered it to starting from resid 1, here we modified it back to start at resid 32
    Nterm_resid = u.residues.resids[0]
    Cterm_resid = u.residues.resids[-1]
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
    for residue in u.residues:
        if residue.resname == "HIS":
            if "HD1" in residue.atoms.names and "HE2" in residue.atoms.names:
                residue.resname = "HSP"
            elif "HD1" in residue.atoms.names and "HE2" not in residue.atoms.names:
                residue.resname = "HSD"
            elif "HD1" not in residue.atoms.names and "HE2" in residue.atoms.names:
                residue.resname = "HSE"
    u.select_atoms("all").write(output_pdb_path)
