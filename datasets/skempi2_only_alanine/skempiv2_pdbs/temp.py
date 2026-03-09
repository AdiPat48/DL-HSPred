from Bio import PDB
import sys

input_pdb = sys.argv[1]
input_chain = sys.argv[2]

# Define a function to extract the sequence, residue numbers, and amino acid types
def extract_sequence_residue_numbers_and_types(pdb_filename):
    parser = PDB.PDBParser(QUIET=True)
    structure = parser.get_structure("protein", pdb_filename)

    # Initialize an empty list to store combined residue info
    residue_info = []

    for model in structure:
        for chain in model:
            if chain.id != input_chain:
                continue
            for residue in chain:
                # Check if the residue is an amino acid (protein)
                if PDB.is_aa(residue):
                    # Get the residue number
                    residue_number = residue.id[1]
                    # Get the one-letter amino acid code
                    amino_acid = PDB.Polypeptide.three_to_one(residue.get_resname())
                    # Combine residue number and amino acid type
                    residue_info.append(f"{residue_number}-{amino_acid}")

    return residue_info

# Replace 'your_pdb_file.pdb' with the path to your PDB file
pdb_file = input_pdb
residue_info = extract_sequence_residue_numbers_and_types(pdb_file)

# Print the combined residue info
for info in residue_info:
    print(info)
