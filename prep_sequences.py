import urllib.request
import io
from Bio import SeqIO

# 1. Download the official human EGFR protein sequence from UniProt (ID: P00533)
url = "https://rest.uniprot.org/uniprotkb/P00533.fasta"
raw_text = urllib.request.urlopen(url).read().decode("utf-8")

# 2. Parse the FASTA text so we can grab just the letters
record = SeqIO.read(io.StringIO(raw_text), "fasta")
full_protein = str(record.seq)

# 3. Slice out ONLY the Kinase Domain (letters 712 to 979)
# Note: Python starts counting at 0, so letter 712 is at index 711
wt_kinase = full_protein[711:979]

# 4. Create the T790M mutant by swapping letter 790 from 'T' to 'M'
# Inside our 712-979 slice, position 790 sits at index 78 (790 - 712 = 78)
mut_kinase = wt_kinase[:78] + "M" + wt_kinase[79:]

# 5. Print both sequences so we can copy them into AlphaFold 3
print("--- WILD-TYPE (Normal) ---")
print(wt_kinase)

print("\n--- T790M MUTANT (Drug-Resistant) ---")
print(mut_kinase)
