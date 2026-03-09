"""
Consensus Hotspot Data Integration and PDB Sequence Parsing

This script merges two distinct hotspot datasets (Aditi's and Vikas') and maps 
identified hotspot residues back to their primary protein sequences using 3D structures.

Key Operations:
1. Loads residue-level labels from 'common_hotspots_forDLModel' and 'consensus_hotspot_GHP.csv'.
2. Parses PDB files from 'all_pdbs/' using Biopython's PDBParser to extract amino acid sequences.
3. Maps identified hotspots to sequence positions, generating a binary label string 
   (1 for hotspot, 0 for nullspot) for each sequence.
4. Outputs the final structured dataset: 'consensus_dataset.csv'.
"""


from Bio import PDB

with open('consensus_dataset.csv','w') as f:
          f.writelines("id,seq,label\n")

# Aditi's Dataset
hs_dict={}

with open('common_hotspots_forDLModel','r') as f:
     for ln in f.readlines():
          pdb_chain_resno=ln.strip()
          pdb_chain=pdb_chain_resno.strip().split("_")[0]+"_"+pdb_chain_resno.strip().split("_")[1]
          resno =pdb_chain_resno.strip().split("_")[2]
          print(pdb_chain, resno)
          if pdb_chain not in hs_dict.keys():
               hs_dict[pdb_chain] = [resno]
          else:
               hs_dict[pdb_chain].append(resno)

# Vikas' Dataset
with open('consensus_hotspot_GHP.csv','r') as f:
     for ln in f.readlines():
          pdb_chain_resno=ln.strip()
          pdb_chain=pdb_chain_resno.strip().split("_")[0]+"_"+pdb_chain_resno.strip().split("_")[1][0]
          resno =pdb_chain_resno.strip().split("_")[1][1:-3]
          print(pdb_chain, resno)
          if pdb_chain not in hs_dict.keys():
               hs_dict[pdb_chain] = [resno]
          else:
               hs_dict[pdb_chain].append(resno)
counter=0
for pdb_chain,res in hs_dict.items():
     counter+=len(res)
print(counter)

# Hotspot processing
counter=0
counter_if=0
for pdb_chain,res in hs_dict.items():
     
     counter_if+=len(res)
     print("hs_dict**************",pdb_chain, res, counter_if)

     input_pdb=pdb_chain.split("_")[0]
     input_chain=pdb_chain.split("_")[1]
     pdb="/home/user/DL_Hotspot/consensus_data/all_pdbs/"+input_pdb+".pdb"
     parser = PDB.PDBParser(QUIET=True)
     structure = parser.get_structure("protein",pdb )
     amino_acid_sequence=""
     label=""
     print("Processing", pdb_chain)
     for model in structure:
          if model.get_id() == 0: # Usually true except for NMR structures
               for chain in model:
                    if chain.id == input_chain:
                         for residue in chain:
                              if residue.get_id()[0] == ' ' and PDB.is_aa(residue):
                                   residue_number = str(residue.id[1])+str(residue.id[2])
                                   residue_number = residue_number.strip()
                                   if residue.get_resname() == "MSE":
                                        amino_acid_sequence+="M"
                                   elif residue.get_resname() == "UNK":
                                        amino_acid_sequence+="X"
                                   else:
                                        amino_acid_sequence+=PDB.Polypeptide.three_to_one(residue.get_resname())
                                   # print("residue_number is", residue_number, res)
                                   if residue_number in res:
                                        counter+=1
                                        print("mal---------------",pdb_chain, residue_number, res, counter)
                                        label+="1"
                                   else:
                                        label+="0"
     
     with open('consensus_dataset.csv','a') as f:
          f.writelines(f'{pdb_chain},{amino_acid_sequence},{label}\n')
