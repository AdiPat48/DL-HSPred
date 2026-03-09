#!/bin/bash

##########################
master_outputfile="ppi_uniprot_all_sequences"
############################

mkdir sequences
for uniprot_id in $(<ppi_uniprot_uniprotids); do
    curl -s -f https://rest.uniprot.org/uniprotkb/${uniprot_id}.fasta -o sequences/${uniprot_id}.fasta
    echo -n "${uniprot_id}," >>  ${master_outputfile} # writing uniprot id to outputfile
    echo -n `grep -v ">" sequences/${uniprot_id}.fasta | sed ':a;N;$!ba;s/\n//g'` >> ${master_outputfile}  # removing header and newline character from fasta ; adding this to outputfile
    echo "" >> ${master_outputfile} #Adding a newline character
done

