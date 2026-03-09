import pandas as pd

ADDED_TOKENS_PER_SEQ = 2
dataset=pd.read_csv('stability.valid.csv')
print(dataset)


seq_col_name = 'seq'
start_seq_len = 2
start_batch_size = 32
increase_factor = 2

seq_len = start_seq_len #512
batch_size = start_batch_size #32

counter=0
while len(dataset) > 0:
    counter+=1
    print("*******************************",counter)
    max_allowed_input_seq_len = seq_len - ADDED_TOKENS_PER_SEQ #512 - 2 = 510
    len_mask = (dataset[seq_col_name].str.len() <= max_allowed_input_seq_len)
    print(len_mask)
    len_matching_dataset = dataset[len_mask]
    print(len_matching_dataset)

    dataset = dataset[~len_mask]
    seq_len *= increase_factor
    # batch_size = max(batch_size // increase_factor, 1)

