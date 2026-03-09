import sys

hs_dict={}

with open('input_hs_dataset.csv','w') as f:
    f.writelines("id,seq,label\n")

with open('ppi_bench_only_alanine_hotspots','r') as f:
    for ln in f.readlines():
        uniprotid_res_resno = ln.strip()
        uniprotid=uniprotid_res_resno.strip().split("_")[0]
        resno=int(uniprotid_res_resno.strip().split("_")[2])
        hs_dict.setdefault(uniprotid, []).append(resno)



with open('ppi_uniprot_all_sequences','r') as f:
    for ln in f.readlines():
        uniprot_id=ln.strip().split(",")[0]
        if not uniprot_id in hs_dict:
            continue
        sequence=ln.strip().split(",")[1]
        label=""
        for i in range(len(sequence)):
            if (i+1) in hs_dict[uniprot_id]:
                label+="1"
            else:
                label+="0"

        with open('input_hs_dataset.csv','a') as f:
            f.writelines(uniprot_id+","+sequence+","+label+"\n")
