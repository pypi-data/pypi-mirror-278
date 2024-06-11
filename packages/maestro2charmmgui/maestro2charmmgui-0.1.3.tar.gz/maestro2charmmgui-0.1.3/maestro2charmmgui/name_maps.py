universal_mod = {"H": "HN"}
Nterm_mod = {"H1": "HT1", "H2": "HT2", "H3": "HT3"}
Cterm_mod = {"O": "OT1", "OXT": "OT2"}
res_mod = {
    "ALA": {},  # No modifications
    "THR": {},  # No modifications
    "VAL": {},  # No modifications
    "ARG": {
        "HB3": "HB2",
        "HB2": "HB1",
        "HD3": "HD2",
        "HD2": "HD1",
        "HG3": "HG2",
        "HG2": "HG1",
    },
    "ASN": {"HB3": "HB2", "HB2": "HB1"},
    "ASP": {"HB3": "HB2", "HB2": "HB1"},
    "CYS": {"HB3": "HB2", "HB2": "HB1", "HG": "HG1"},
    "GLN": {"HB3": "HB2", "HB2": "HB1", "HG3": "HG2", "HG2": "HG1"},
    "GLU": {"HB3": "HB2", "HB2": "HB1", "HG3": "HG2", "HG2": "HG1"},
    "GLY": {"HA3": "HA2", "HA2": "HA1"},
    "HIS": {"HB3": "HB2", "HB2": "HB1"},
    "ILE": {
        "CD1": "CD",
        "HD11": "HD1",
        "HD12": "HD2",
        "HD13": "HD3",
        "HG13": "HG12",
        "HG12": "HG11",
    },
    "LEU": {"HB3": "HB2", "HB2": "HB1"},
    "LYS": {
        "HB3": "HB2",
        "HB2": "HB1",
        "HD3": "HD2",
        "HD2": "HD1",
        "HE3": "HE2",
        "HE2": "HE1",
        "HG3": "HG2",
        "HG2": "HG1",
    },
    "MET": {"HB3": "HB2", "HB2": "HB1", "HG3": "HG2", "HG2": "HG1"},
    "PHE": {"HB3": "HB2", "HB2": "HB1"},
    "PRO": {
        "HB3": "HB2",
        "HB2": "HB1",
        "HD3": "HD2",
        "HD2": "HD1",
        "HG3": "HG2",
        "HG2": "HG1",
    },
    "SER": {"HB3": "HB2", "HB2": "HB1", "HG": "HG1"},
    "TRP": {"HB3": "HB2", "HB2": "HB1"},
    "TYR": {"HB3": "HB2", "HB2": "HB1"},
}
