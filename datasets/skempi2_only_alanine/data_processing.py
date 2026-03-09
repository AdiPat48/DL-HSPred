
from Bio import PDB

with open('input_ns_dataset.csv','w') as f:
          f.writelines("id,seq,label\n")

ns_dict={}
with open('/home/user/DL_Hotspot/dataset_060523/skempi2_only_alanine/pdb_sequences_not_uniprot/clustering_pdb_sequences/clustered_pdbseq_skempi2_ns_only_alanine','r') as f:
     for ln in f.readlines():
          pdb_chain_res_resno=ln.strip()
          skempi2_pdb_chain=pdb_chain_res_resno.strip().split("_")[0]+"_"+pdb_chain_res_resno.strip().split("_")[1]
          skempi2_resno =pdb_chain_res_resno.strip().split("_")[3]
          if skempi2_pdb_chain not in ns_dict.keys():
               ns_dict[skempi2_pdb_chain] = [skempi2_resno]
          else:
               ns_dict[skempi2_pdb_chain].append(skempi2_resno)



# Nullspot processing

for pdb_chain,res in ns_dict.items():
     input_pdb=pdb_chain.split("_")[0]
     input_chain=pdb_chain.split("_")[1]
     skempi2_pdb="/home/user/DL_Hotspot/dataset_060523/skempi2_only_alanine/skempiv2_pdbs/"+input_pdb+".pdb"
     parser = PDB.PDBParser(QUIET=True)
     structure = parser.get_structure("protein",skempi2_pdb )
     amino_acid_sequence=""
     label=""
     for model in structure:
          for chain in model:
               if chain.id == input_chain:
                    for residue in chain:
                         if PDB.is_aa(residue):
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
                                   label+="9"
                              else:
                                   label+="0"
     
     with open('input_ns_dataset.csv','a') as f:
          f.writelines(f'{pdb_chain},{amino_acid_sequence},{label}\n')
