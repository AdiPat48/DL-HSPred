# Checks whether the reported residue number corresponds to the same residue in pdb sequence

import sys
from Bio import PDB


pdb_chain_res_resno = sys.argv[1]

#print(f"###################\n{pdb_chain_res_resno}\n###################")
skempi2_pdb="skempiv2_pdbs/"+pdb_chain_res_resno.strip().split("_")[0]+".pdb"
skempi2_chain=pdb_chain_res_resno.strip().split("_")[1]
skempi2_res=pdb_chain_res_resno.strip().split("_")[2]
skempi2_resno =pdb_chain_res_resno.strip().split("_")[3]



parser = PDB.PDBParser(QUIET=True)
structure = parser.get_structure("protein",skempi2_pdb )

for model in structure:
     for chain in model:
          if chain.id != skempi2_chain:
               continue
          for residue in chain:
               # Get the residue number
               residue_number = residue.id[1]
               if residue_number == skempi2_resno:
                    # Get the one-letter amino acid code
                    amino_acid = PDB.Polypeptide.three_to_one(residue.get_resname())
                    if not amino_acid==skempi2_res:
                         print(pdb_chain_res_resno, ";",amino_acid)
                    # if amino_acid==skempi2_res:
                    #      print("Correct", pdb_chain_res_resno, ";",amino_acid)

                    
					
                