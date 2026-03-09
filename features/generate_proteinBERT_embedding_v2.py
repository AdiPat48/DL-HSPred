"""
ProteinBERT Feature Extraction Engine

Transforms raw protein sequences into high-dimensional feature vectors (embeddings) 
using a pre-trained ProteinBERT language model.

Workflow:
1. Loads the consensus dataset and calculates the maximum sequence length for padding.
2. Encodes sequences for ProteinBERT, including START and END tokens.
3. Extracts 1562-dimensional local representations (residue-level embeddings).
4. Handles START token padding for labels and converts nullspot placeholders (label 9) 
   to binary classification format (label 0).
5. Saves extracted residue-level embeddings and labels as a flattened CSV for model training.

Dependencies: tensorflow, proteinbert, pandas, numpy
"""

import tensorflow as tf
import os , sys
import pandas as pd
import numpy as np
from proteinbert import OutputType, OutputSpec, FinetuningModelGenerator, load_pretrained_model, finetune, evaluate_by_len
from proteinbert.conv_and_global_attention_model import get_model_with_hidden_layers_as_outputs

#dataset=pd.read_csv('/home/aditipathak/DL_Hotspot/datasets/combined_input_dataset.csv')
dataset=pd.read_csv(sys.argv[1]) 
def generate_proteinBERT_embeddings(dataset):
	
	# Calculate the length of each string in the specified column and find the maximum length
	max_seq_length = dataset['seq'].str.len().max()

	# Print the maximum length
	print("Length of the longest sequence:", max_seq_length)

	data = dataset['seq']
	labels = np.array(dataset['label'].apply(lambda x: list(map(int, list(str(x))))).values)



	#Loading the pretrained protein_bert model
	pretrained_model_generator, input_encoder = load_pretrained_model( local_model_dump_dir='/home/aditipathak/DL_Hotspot/scripts/')

	#Creating a model for given sequence length
	seq_len= max_seq_length + 2      # for start and end token
	
	
	model = get_model_with_hidden_layers_as_outputs(pretrained_model_generator.create_model(seq_len))


	#Encoding sequences
	X = input_encoder.encode_X(data, seq_len)

	#Generating embedding
	local_representations, global_representations= model.predict(X, batch_size = 16)
	local_representations = np.array(local_representations)

	print(local_representations.shape) # OUTPUT: (211, 3048, 1562)


	# Adding a 0 to the start of each label to account for START token in proteinBERT embedding  
	labels_padded = []

	for label in labels:
		label_padded = np.pad(label, (1, seq_len - len(label) -1 ), mode='constant', constant_values=0)
		labels_padded.append(label_padded)
	labels_padded = np.array(labels_padded)

	print(labels_padded.shape) # OUTPUT:(211, 3048)


	# Extracting only HS and NS residue embeddings (local representations) along with corresponding labels (updated_labels)
	# NS label "9" has been replaced with "0"
	nonzero_reduced_matrix = []
	updated_labels = []
	ids=[]
	for seq in range(0,len(local_representations)):
		for aa in range(len(local_representations[seq])):
			if int(labels_padded[seq][aa]) == 0:
				continue
			else:
				nonzero_reduced_matrix.append(local_representations[seq][aa])
				updated_labels.append(labels_padded[seq][aa])
				resnum = str(aa)
				resname = data[seq][aa-1] # Since we have a START token in the embedding (local representation)
				ids.append(dataset['id'][seq]+"_"+resname+"_"+resnum) 

	print("nonzero_reduced_matrix.shape ", np.array(nonzero_reduced_matrix).shape) # OUTPUT: nonzero_reduced_matrix.shape  (735, 1562)

	updated_labels = [0 if y==9 else y for y in updated_labels]
	print("updated_labels.shape",np.array(updated_labels).shape) # OUTPUT: updated_labels.shape (735,)
	print("updated_labels = ", updated_labels[:20]) # OUTPUT: updated_labels =  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	print("updated_labels = ", updated_labels[-20:]) # OUTPUT: updated_labels =  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

	# Concatenate the nonzero_reduced_matrix(embeddings) and updated_labels along the columns (axis=1) to create a DataFrame

	updated_labels_dict = {'label': updated_labels}
	ids_dict = {'ID': ids}
	# Concatenate the two DataFrames 
	df = pd.concat([pd.DataFrame(ids_dict), pd.DataFrame(nonzero_reduced_matrix), pd.DataFrame(updated_labels_dict)], axis=1)

	print(df.head(5))

	"""
	OUTPUT:
	ID         0         1         2         3         4         5         6         7  ...      1554      1555      1556      1557          1558          1559          1560          1561  label
	0  1A22_A_H_18  0.041843  0.039586 -0.009501 -0.526758  0.269531 -0.171651  0.064260 -0.152808  ...  0.003485  0.000768  0.000009  0.002497  2.793807e-11  5.502131e-08  6.005084e-08  3.593793e-10      0
	1  1A22_A_H_21 -0.037234  0.247257 -0.009700 -0.573698  0.020038  0.013687  0.147256 -0.236744  ...  0.004430  0.000996  0.000004  0.003303  5.908435e-12  4.322382e-08  2.599580e-07  3.466741e-10      0
	2  1A22_A_Q_22  0.198116 -0.092158  0.097526 -0.805329  0.092765  0.012063 -0.057102 -0.170418  ...  0.001161  0.000251  0.000005  0.000763  1.968167e-13  1.190303e-08  4.461937e-08  3.250527e-10      0
	3  1A22_A_F_25  0.001969  0.335273 -0.098158 -0.774519 -0.150158  0.186159 -0.144428 -0.208741  ...  0.003329  0.000704  0.000004  0.001852  1.127271e-10  2.509429e-08  2.661037e-08  1.341287e-10      0
	4  1A22_A_Y_42 -0.071298 -0.098551 -0.190240 -0.827787 -0.024964 -0.092479 -0.177154 -0.088284  ...  0.003814  0.000854  0.000005  0.935652  7.969173e-11  3.185834e-08  5.543358e-08  3.179614e-10      0

	[5 rows x 1564 columns]

	"""

	df.to_csv(f'embedded_{sys.argv[1].split("/")[-1].split(".")[0]}.csv', index=False)
	print(f'embedded_{sys.argv[1].split("/")[-1].split(".")[0]}.csv written')

generate_proteinBERT_embeddings(dataset)


