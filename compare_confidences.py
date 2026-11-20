import glob
import json
from pathlib import Path

def inspect_folder(label: str, folder_path: str) -> None:
    folder = Path(folder_path)
    json_files = sorted(folder.glob("*summary_confidences*.json"))

    print(f"\n=== {label} ({len(json_files)} models found) ===")
    if not json_files:
        print(f"No summary confidence JSON files found in '{folder_path}'.")
        return

    for path in json_files:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        ptm = data.get("ptm")
        iptm = data.get("iptm")
        ranking = data.get("ranking_score")
        clash = data.get("has_clash")

        print(
            f"{path.name}: "
            f"ranking_score={ranking:.3f} | "
            f"pTM={ptm:.3f} | "
            f"ipTM={iptm:.3f} | "
            f"has_clash={clash}"
        )

if __name__ == "__main__":
    # Update folder names if your extracted folders have slightly different names
    wt_matches = glob.glob("*wt*atp*") or glob.glob("*WT*ATP*")
    mut_matches = glob.glob("*t790m*atp*") or glob.glob("*T790M*ATP*")

    wt_dir = next((p for p in wt_matches if Path(p).is_dir()), "EGFR_WT_ATP")
    mut_dir = next((p for p in mut_matches if Path(p).is_dir()), "EGFR_T790M_ATP")

    inspect_folder("WILD-TYPE + ATP + Mg2+", wt_dir)
    inspect_folder("T790M MUTANT + ATP + Mg2+", mut_dir)
