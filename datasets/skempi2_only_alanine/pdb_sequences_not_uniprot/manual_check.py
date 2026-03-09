# Checks whether the reported residue number corresponds to the same residue in pdb sequence

import os, sys
import pandas as pd


pdb_chain_res_resno = sys.argv[1] 
skempi2_pdb_chain=pdb_chain_res_resno[:6]
skempi2_resno =int(pdb_chain_res_resno.strip().split("_")[-1])
skempi2_res=pdb_chain_res_resno.strip().split("_")[2]

with open('skempi2_nullspots_all_pdb_sequences','r') as f:
     for ln in f.readlines():
          pdb_chain=ln.strip().split(",")[0]
          sequence=ln.strip().split(",")[1]
          if pdb_chain == skempi2_pdb_chain:
            if not sequence[skempi2_resno-1]==skempi2_res:
            	print(f'Skempi2 residue: {skempi2_res} ;',f'Pdb sequence residue: {sequence[skempi2_resno-1]}')
					
                