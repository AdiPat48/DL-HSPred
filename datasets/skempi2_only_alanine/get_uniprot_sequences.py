import os, sys
import pandas as pd


#INPUTS
#CSV File from pdb advanced search
input_csv='edited_rcsb_pdb_sequence_20230907051234.csv' 
#File with PDB and Chain to be submitted
input_pc='pdb_chain_skempi2_nullspots_only_alanine'

#OUTPUTS
outputfile='skempi2_nullspots_sequence_source.csv'
sequence_masterfile = 'skempi2_nullspots_all_sequences'

if not os.path.isfile(outputfile):
	with open(outputfile,'a') as f:
		f.writelines("PDB_chain,sequence_source,id\n")




#Getting pdb and chain combinations from skempi2 only ala nullspots
pdb_chain_combination_list=[]
with open(input_pc,'r') as f:
	for ln in f.readlines():
		pdb_chain=ln.strip()
		pdb_chain_combination_list.append(pdb_chain)


df = pd.read_csv(input_csv,header=1)

#Updating Entry_ID so that the blank fields are replaced with the corresponding PDB ids
updated_EntryID=[]
for x in df['Entry ID']:
	if not pd.isna(x):
		pdb=x
	updated_EntryID.append(pdb)

df['Entry ID']=updated_EntryID
print(df)

#Getting all possible pdb_chain combinations from the advanced search csv file and putting it in a dictionary where :
# key = pdb_chain and value = uniprot id	
pdb_chain_uniprot_dict={}
pdb_chain_pdbsequence_dict={}
for i in range(len(df['Entry ID'])):
	pdb=df['Entry ID'][i]	
	print(i,df['Auth Asym ID'][i])
	for chain in df['Auth Asym ID'][i].split(", "):
		key=pdb+"_"+chain
		pdb_chain_uniprot_dict[key]=df['Accession Code(s)'][i]
		pdb_chain_pdbsequence_dict[key]=df['Sequence'][i]




#Getting uniprot ids of BID combinations		
for x in pdb_chain_combination_list:
	uniprot_id=str(pdb_chain_uniprot_dict[x])
	print(x, uniprot_id)
	
	if len(uniprot_id)<6:
		sequence=">"+x+"\n"+pdb_chain_pdbsequence_dict[x]
		sequence_source="pdb"
		with open(("./sequences/"+x+".fasta"),'w') as o:
			o.writelines(sequence)
		with open(sequence_masterfile,'a') as masterfile:
			masterfile.writelines(f'{x},{pdb_chain_pdbsequence_dict[x]}\n')

	else:
		sys_out=str(os.system("curl -s -f https://rest.uniprot.org/uniprotkb/"+uniprot_id+".fasta -o sequences/"+x+".fasta"))[:-1]
		sequence_source="uniprot"
		with open(f"sequences/{x}.fasta",'r') as sequ:
			sequence="".join([ln.strip() for ln in sequ.readlines() if not ">" in ln])
		with open(sequence_masterfile,'a') as masterfile:
			masterfile.writelines(f'{x},{sequence}\n')
	

	with open(outputfile,'a') as f:
		f.writelines(x+","+sequence_source+","+uniprot_id+"\n")
	

	


	
	
	

	
	
	
	
	
	
