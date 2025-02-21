import os
import sys
import subprocess
import numpy as np
from rdkit import Chem
cwd = print(os.getcwd())
PATH_ADFR = sys.argv[1]
filename = sys.argv[2]
molname = filename.replace('.mol2','')
print(filename)

HOME = "/home/biomd"

os.system(f"{PATH_ADFR}/prepare_ligand -l {filename} -C")
mol = Chem.MolFromMol2File(filename, removeHs= False)
mol = mol.GetAtoms()
print(len(mol))
input_mol = np.empty((len(mol), 2), dtype=object)
pdbqt_info = subprocess.getoutput(f"gawk '/ATOM/ {{print $3, $12}}' {molname}.pdbqt").split('\n')
pdbqt_info = np.array([line.split() for line in pdbqt_info])
# print(pdbqt_info)
for idx, at in enumerate(mol):
    atname = at.GetProp('_TriposAtomName')
    input_mol[idx,0] = atname
    try:
        index_ofname = np.where(pdbqt_info == atname)[0][0]
    except IndexError:
        continue
    charge = pdbqt_info[index_ofname,1]
    input_mol[idx,1] = charge
        
# for idx in reversed(range(len(input_mol))):
#     if(input_mol[idx,1] is None):
#         input_mol = np.delete(input_mol, idx,0)

print(input_mol)
watname = f"{molname}_wat_ligand.pdbqt"
# Had to install develop branch of Meeko because the release is bugged!
os.system(f"mk_prepare_ligand.py -i {filename} -o map_{watname} --add_index_map")
os.system(f"mk_prepare_ligand.py -i {filename} -w -o {watname} --add_index_map")
genmap = 1
if(genmap):
    mapstring = subprocess.getoutput(f"awk '/REMARK INDEX MAP/ {{for (i=4; i<=NF; i++) print $i}}' map_{watname}")
    mapstring = mapstring.split('\n')
    i=0
    maps = np.zeros((len(mapstring)//2,2), dtype = int)
    for i in range(0,len(mapstring),2):
        j = i//2
        # print(mapstring)
        maps[j,0],maps[j,1] = mapstring[i],mapstring[i+1]
    # print(maps)
maps_opt = [[i[0], i[1]] for i in maps]
np.savetxt("map.txt", maps_opt, fmt='%d')

mapstring = subprocess.getoutput(f"awk '/REMARK INDEX MAP/ {{for (i=4; i<=NF; i++) print $i}}' {watname}")
mapstring = mapstring.split('\n')
i=0
maps = np.zeros((len(mapstring)//2,2), dtype = int)
for i in range(0,len(mapstring),2):
    j = i//2
    maps[j,0],maps[j,1] = mapstring[i],mapstring[i+1]
# print(maps)


TAG1 = '@<TRIPOS>ATOM'
TAG2 = '@<TRIPOS>BOND'

os.system(f"cp {watname} {molname}_wat_charged_temp.pdbqt")
for pair in maps:
    idx0 = pair[0]
    idx1 = pair[1]
    charge = input_mol[idx0-1, 1]
    atom_name = input_mol[idx0-1, 0]
    # print(idx0, idx1,charge)
    old = subprocess.getoutput(f"gawk '/ATOM/ && $2=={idx1}' {molname}_wat_charged_temp.pdbqt")
    # l = subprocess.getoutputs(f"gawk '/ATOM/ && $2=={idx1} {{print}}' {molname}_wat_charged.pdbqt")
    # print(idx1, old)>
    # change charge
    if charge is None:
        print(f"{atom_name}, {charge}, {pair}, {old}")
    line_charge = old.replace(old.split()[-2], charge)
    if(line_charge[70] == ' '):
        line_charge = line_charge[:70:] + line_charge[71:]
    if(line_charge.split()[-2][0]!='-'):
        line_charge = line_charge[:69] +' '+ line_charge[69:]
    # print(l)
    # Be careful with lines!!!
        
    l = line_charge.replace(f"{line_charge.split()[-10]}  ", f"{atom_name}" + " "*(3-len(atom_name)) )
    os.system(f"gawk '/ATOM/ && $2=={idx1} {{gsub(/{old}/, \"{l}\")}} 1' {molname}_wat_charged_temp.pdbqt > {molname}_wat_charged.pdbqt")
    os.system(f"cp {molname}_wat_charged.pdbqt {molname}_wat_charged_temp.pdbqt")
    # print(l)
