import sys
import statistics
import numpy
inputfile='skempi_v2.csv' #Original
hs_dict={}
ns_dict={}
unique_pdb_chain_combinations=[]
line_no=0
with open (inputfile,'r') as f:
    for ln in f.readlines():
        line_no+=1
        if ln.startswith("#"):
            continue
        if len(ln.split(";")[1].split(','))>1: #Getting entries with only single mutations reported - Why?
            continue
        pdb=ln.split(";")[0].split("_")[0]       
        residue=ln.split(";")[1]
        chain=residue[1]
        
        if not residue[-1]=="A":
             continue 	       
        
        res_no=residue[0:1]+residue[2:]
        location=ln.split(";")[3]
        t=ln.split(";")[13]
        Kd_mut=ln.split(";")[7]
        Kd_wt=ln.split(";")[9]
        

        if "" in [t,Kd_mut,Kd_wt]:
            continue

        if location=="INT" or location=="SUR" or location=="": #mutations which are the interior (INT), surface (SUR) of the protein
            continue
        if (t[0].isdigit() and Kd_mut[0].isdigit() and Kd_wt[0].isdigit()):
            t=float(ln.split(";")[13].split("(")[0])
            Kd_mut=float(ln.split(";")[7])
            Kd_wt=float(ln.split(";")[9])
            R= 8.314/4184 #Gas constant in kcal K(-1) mol(-1)
            t= t
            dG_mut= R*t*(numpy.log(Kd_mut))
            dG_wt= R*t*(numpy.log(Kd_wt))
            ddG= abs(dG_mut - dG_wt)
            key=pdb+"_"+residue
#            key=pdb+"_"+chain+"_"+res_no
            if ddG>0 and ddG<1 :
                if not key in ns_dict.keys():
                    ns_dict[key]=[ddG]
                else:
                    ns_dict[key].append(ddG)
                
                	
            if ddG>=2.0 :
                if not key in hs_dict.keys():
                    hs_dict[key]=[ddG]
                else:
                    hs_dict[key].append(ddG)                   
                

# with open('skempi2_hs_avgddG_only_skempi2.txt','w') as f:
#     for x in hs_dict.keys():
#         f.writelines(x +","+ str(statistics.mean(hs_dict[x]))+"\n")

# with open('skempi2_ns_avgddG_only_skempi2.txt','w') as f:
#     for x in ns_dict.keys():
#         f.writelines(x +","+ str(statistics.mean(ns_dict[x]))+"\n")

with open('skempi2_hs_maxgddG_only_alanine.txt','w') as f: # Taking the maximum ddG reported
    for x in hs_dict.keys():
        print(x, hs_dict[x])
        f.writelines(x +","+ str(max(hs_dict[x]))+"\n")

with open('skempi2_ns_maxddG_only_alanine.txt','w') as f:
    for x in ns_dict.keys():
        print(x, ns_dict[x])
        f.writelines(x +","+ str(max(ns_dict[x]))+"\n")       

with open('skempi2_hs_only_alanine.txt','w') as f:
    for x in hs_dict.keys():
        pdb=x.split("_")[0]
        chain=x.split("_")[1][1]
        res_no=x.split("_")[1][2:-1]
        res=x.split("_")[1][0]
        f.writelines(pdb+"_"+chain+"_"+res+"_"+res_no+"\n")

with open('skempi2_ns_only_alanine.txt','w') as f:
    for x in ns_dict.keys():
        pdb=x.split("_")[0]
        chain=x.split("_")[1][1]
        res_no=x.split("_")[1][2:-1]
        res=x.split("_")[1][0]
        f.writelines(pdb+"_"+chain+"_"+res+"_"+res_no+"\n")
        
