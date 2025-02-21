import numpy as np
import sys
import os
import fileinput


PYTHONSH = sys.argv[1]
FILENAME = sys.argv[2]
NAME = FILENAME.split('.')[0].split('_')[0]
protein = sys.argv[3]
protname = protein.split(".")[0]
ligand = sys.argv[4]
SIZE = int(sys.argv[5])
if len(sys.argv)>6:
	FOLDNAME = sys.argv[6]
else:
	FOLDNAME = "grid_site"
	
	
HOME = "/home/biomd"

def editfile(filename):
	idx=None
	shift = 0
	for line in fileinput.FileInput(filename, inplace=True):
		if (shift):
			idx = int(line.split()[1])
			line = line.replace(f"variable {idx}", f"variable {idx+1}")
		if "S-affinity" in line:
			line += "label=W-affinity" + os.linesep
		if "S.map" in line:
			idx = int(line.split()[1])
			oldline = line
			oldline = oldline.replace(".S.", ".W.")
			oldline = oldline.replace(f"variable {idx}", f"variable {idx+1}")
			line += oldline
			shift=1
		print(line, end="")


centers = np.genfromtxt(FILENAME, dtype='str', skip_header=1)
if len(centers.shape) == 1:
    centers = [np.array(centers[1:], dtype=float)]
else:
    centers = np.array(centers[:, 1:], dtype=float)
num = len(centers)
print(num)
i=0
for line in centers:
	line = np.array(line, dtype=str)
	gridcenter = f"{line[0]} {line[1]} {line[2]}"
	print(gridcenter)
	os.system(f"mkdir {FOLDNAME}{i+1}")
	os.system(f"cp {protein} {FOLDNAME}{i+1}/{i+1}_{protein}")
	os.system(f"cp {ligand} {FOLDNAME}{i+1}/{i+1}_{ligand}")
	os.chdir(f"{FOLDNAME}{i+1}")
	
	if(ligand.split("_wat_charged")[0] == "znthpp"):
		print("Using Zn forcefield")
		os.system(f"{PYTHONSH} ../dock_py/prepare_gpf4zn.py -l {i+1}_{ligand} -r {i+1}_{protein} -p npts='{SIZE},{SIZE},{SIZE}' -p gridcenter='{gridcenter}' -p ligand_types='A,NA,C,HD,N,OA,S,SA,ZN'  -o {i+1}_{protname}.gpf")
	else:
		print("Using normal forcefield")
		os.system(f"{PYTHONSH} ../dock_py/prepare_gpf.py -l {i+1}_{ligand} -r {i+1}_{protein} -p npts='{SIZE},{SIZE},{SIZE}' -p gridcenter='{gridcenter}' -p ligand_types='A,NA,C,HD,N,OA,S,SA'  -o {i+1}_{protname}.gpf")
	os.system(f"autogrid4 -p {i+1}_{protname}.gpf -l {i+1}_{protname}.glg")
	os.system(f"python3 ../dock_py/mapwater.py -r {i+1}_{protname} -s {i+1}_{protname}.W.map")
	
	editfile(f"{i+1}_{protname}.maps.fld")
	os.chdir("..")
	i+=1
print(centers)
