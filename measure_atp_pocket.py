import glob
from pathlib import Path
from Bio.PDB import MMCIFParser

def find_top_cif(folder_path: str) -> Path:
    folder = Path(folder_path)
    # AlphaFold Server names the top-ranked structure *model_0.cif
    matches = sorted(folder.glob("*model_0.cif"))
    if not matches:
        raise FileNotFoundError(f"No *_model_0.cif found in '{folder_path}'")
    return matches[0]

def min_distance_to_atp(cif_path: Path, target_resseq: int) -> float:
    parser = MMCIFParser(QUIET=True)
    structure = parser.get_structure("complex", str(cif_path))
    model = next(structure.get_models())

    target_atoms = []
    atp_atoms = []

    for chain in model:
        for residue in chain:
            hetflag, resseq, _ = residue.id
            resname = residue.get_resname().strip()

            # Target protein residue (standard polymer residue, hetflag == " ")
            if hetflag == " " and resseq == target_resseq:
                for atom in residue:
                    # Skip hydrogens (element 'H' or 'D')
                    if atom.element.strip() not in ("H", "D"):
                        target_atoms.append(atom)

            # Bound ATP ligand
            if resname == "ATP":
                for atom in residue:
                    if atom.element.strip() not in ("H", "D"):
                        atp_atoms.append(atom)

    if not target_atoms:
        raise ValueError(f"Residue {target_resseq} not found in {cif_path.name}")
    if not atp_atoms:
        raise ValueError(f"ATP not found in {cif_path.name}")

    min_dist = float("inf")
    for p_atom in target_atoms:
        for a_atom in atp_atoms:
            # Biopython Atom subtraction returns Euclidean distance in Angstroms (Å)
            dist = p_atom - a_atom
            if dist < min_dist:
                min_dist = dist

    return min_dist

if __name__ == "__main__":
    wt_matches = glob.glob("*wt*atp*") or glob.glob("*WT*ATP*")
    mut_matches = glob.glob("*t790m*atp*") or glob.glob("*T790M*ATP*")

    wt_dir = next((p for p in wt_matches if Path(p).is_dir()), "EGFR_WT_ATP")
    mut_dir = next((p for p in mut_matches if Path(p).is_dir()), "EGFR_T790M_ATP")

    wt_cif = find_top_cif(wt_dir)
    mut_cif = find_top_cif(mut_dir)

    # Position 79 in our 268-aa kinase domain = full-length EGFR 790
    wt_dist = min_distance_to_atp(wt_cif, target_resseq=79)
    mut_dist = min_distance_to_atp(mut_cif, target_resseq=79)

    print(f"WT ({wt_cif.name}) min distance from res 79 to ATP:    {wt_dist:.2f} Å")
    print(f"T790M ({mut_cif.name}) min distance from res 79 to ATP: {mut_dist:.2f} Å")
