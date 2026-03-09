import sys

uniprotid_res_resno = sys.argv[1]
ppidb_uniprotid=uniprotid_res_resno.strip().split("_")[0]
ppidb_res=uniprotid_res_resno.strip().split("_")[1]
ppidb_resno=int(uniprotid_res_resno.strip().split("_")[2])


with open('ppi_uniprot_all_sequences','r') as f:
    for ln in f.readlines():
        uniprot_id=ln.strip().split(",")[0]
        if uniprot_id==ppidb_uniprotid:
            sequence=ln.strip().split(",")[1]
            if not sequence[ppidb_resno-1]==ppidb_res:
                print(uniprotid_res_resno,f'; Residue in sequence : {sequence[ppidb_resno]} ')