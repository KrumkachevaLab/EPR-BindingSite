# This helper script takes the .mol2 file of the ligand to be docked and generates both .pdbqt files for docking and GAFF2 topologies for the MD
# In this version 

import sys
import os
NAME_mol2 = sys.argv[1] # Name of the .mol2 file
NAME = NAME_mol2.split(".mol2")[0]
PATH_TO_DOCKING = sys.argv[2] # Path of the working docking directory
PATH_TO_MD = sys.argv[3] # Path of the working MD directory
SCRIPT_LIGAND = sys.argv[4] # Path to the script for the generation of .pdbqt ligand file for docking
PATH_ADFR = sys.argv[5] # Path to ADFR/bin
acpype_path = f"/home/biomd/Documents/GitHub/acpype/run_acpype.py"
os.system(f"echo Paths are {NAME=} {PATH_TO_DOCKING=} {PATH_TO_MD=} {SCRIPT_LIGAND=}")

# -r option is currently NOT implemented in acpype, pull request in pending
# print(f"{acpype_path} -i {NAME_mol2} -c user -f -r 1")
# os.system(f"{acpype_path} -i {NAME_mol2} -c user -f -r 5")

os.system(f"{acpype_path} -i {NAME_mol2} -c user -f")

acpype_folder = f"{NAME}.acpype"
os.system(f" echo Generated GAFF2 topologies for {NAME}!")


os.system(f"mkdir {NAME}_export")
os.system(f"cp {acpype_folder}/{NAME}_user_gaff2.mol2 {NAME}_export/{NAME}_gaff.mol2")
os.system(f"cp {NAME}.mol2 {NAME}_export/{NAME}.mol2")
os.system(f"cp {acpype_folder}/{NAME}_GMX.itp {NAME}_export/{NAME}_GMX.itp")
os.system(f"cp {acpype_folder}/posre_{NAME}.itp {NAME}_export/posre_{NAME}.itp")

os.system(f"cp {NAME}_export/{NAME}.mol2 {PATH_TO_DOCKING}/")
# os.system(f"cp {NAME}_export/posre_{NAME}.itp {NAME}_export/{NAME}_GMX.itp {PATH_TO_MD}/")
os.system(f"echo Moved resulting files in folders for {NAME}!")

os.chdir(PATH_TO_DOCKING)
os.system(f"python3 {SCRIPT_LIGAND} {PATH_ADFR} {NAME}.mol2")