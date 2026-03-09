import pandas as pd


df_hs= pd.read_csv('/home/user/DL_Hotspot/dataset_060523/PPI_hotspotdb/input_hs_dataset.csv')
df_ns = pd.read_csv('input_ns_dataset.csv') 


for i in range(len(df_ns)):
    pdb_sequence = df_ns['amino_acid_sequence'][i]
    pdb_id = df_ns['pdb_chain'][i]
    for x in range(len(df_hs['sequence'])):
        uniprot_seq = df_hs['sequence'][x]
        uniprot_id = df_hs['uniprot_id'][x]
        #print(uniprot_id, uniprot_seq)
        if pdb_sequence == uniprot_seq:
            print(pdb_id,uniprot_id)

    