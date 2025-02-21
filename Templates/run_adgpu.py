import numpy as np
import sys
import os
import glob
import subprocess

protein = sys.argv[1]
ligand = sys.argv[2]
nrun = int(sys.argv[3])
ifgenrun = int(sys.argv[4])

if len(sys.argv)>5:
	FOLDNAME = sys.argv[5]
else:
	FOLDNAME = "grid_site"
	
if len(sys.argv)>6:
	HEURMAX = sys.argv[6]
else:
	HEURMAX = None

protname = protein.split(".")[0]

pwd = os.getcwd()
centers = glob.glob(f"{pwd}/{FOLDNAME}*")
print(centers)
i=0
for cent in centers	:
	os.chdir(f"{FOLDNAME}{i+1}")
	print(f"adgpu --lfile {i+1}_{ligand} --ffile {i+1}_{protname}.maps.fld --gbest 1 --npdb {ifgenrun} --nrun {nrun} -p 2048 --rmstol 3 --derivtype Zn=ZN")
	if HEURMAX is None:
		os.system(f"adgpu --lfile {i+1}_{ligand} --ffile {i+1}_{protname}.maps.fld --gbest 1 --npdb {ifgenrun} --nrun {nrun} -p 2048 --rmstol 3 --derivtype Zn=ZN")
	else:
		os.system(f"adgpu --lfile {i+1}_{ligand} --ffile {i+1}_{protname}.maps.fld --gbest 1 --npdb {ifgenrun} --nrun {nrun} -p 2048 --rmstol 3 --derivtype Zn=ZN  --heurmax {HEURMAX}")
	os.system("echo Autodock finished!")
	energy = subprocess.getoutput("awk '/RANKING/ {if ($1==1 && $2==1) print $4;}' *.dlg")
	os.system(f"cp best.pdbqt ../{i+1}_best_{energy}.pdbqt")
	print(energy)
	runs = glob.glob(f"{os.getcwd()}/*_run*")
	runs.sort()
	for run in runs:
		name = run.split("/")[-1].split(".pdbqt")[0]
		idx = int(name.split("run")[1].split("_")[0])
		run_energy = subprocess.getoutput(f"awk '/RANKING/ {{if ($3 == {idx}) print $4;}}' *.dlg")
		os.system(f"mv {name}.pdbqt run{idx}_{run_energy}.pdbqt")
	# GET CLUSTERS
	clusters = subprocess.getoutput("xmllint --xpath '//result/clustering_histogram/cluster' *.xml")
	# print(clusters)
	clusters = clusters.split("\n")
	# print(clusters)
	cluster = np.empty(len(clusters),dtype = int)
	run_energy = np.empty(len(clusters),dtype = float)
	run = np.empty(len(clusters),dtype = int)
	nclust = np.empty(len(clusters),dtype = int)
	for idx, cl in enumerate(clusters):
		cl = cl.split()
		cluster[idx] = cl[1].split("=")[1].replace('"','')
		run_energy[idx] = cl[2].split("=")[1].replace('"','')
		run[idx] = cl[3].split("=")[1].replace('"','')
		nclust[idx] = cl[5].split("=")[1].replace("/>",'').replace('"','')
		os.system(f"cp run{run[idx]}_{format(run_energy[idx],'.2f')}.pdbqt cluster{cluster[idx]}_{run_energy[idx]}_p{nclust[idx]}.pdbqt")
	os.chdir("..")
	i+=1
print(centers)
