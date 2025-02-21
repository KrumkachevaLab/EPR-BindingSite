Please note that while the provided code is not adapted for easy setup on different computers yet.
# To-Do
1. Fix the relationship between different files
2. Provide an example of the calculations (HSA-TCPP)
# Protein-Ligand Binding Site Identification Based on Dipolar EPR Experiments
This project contains Jupyter Notebooks designed to identify binding sites in protein-ligand complexes using dipolar EPR distance distributions. The methodology is based on the approach described in the upcoming publication "Enhanced Binding Site Detection in Protein-Ligand Complexes with a Combined Blind Docking and Dipolar EPR Approach" (to be published).


## Repository Contents
This repository includes three Jupyter Notebooks used for the binding site identification using dipolar EPR data.
## Required Software
This approach relies on AutoDock-GPU for both blind and focused docking. You can find AutoDock-GPU at:
https://github.com/ccsb-scripps/AutoDock-GPU

After installing AutoDock-GPU, make sure to specify the path to its executable file within the Jupyter Notebook for docking.
## Required Python Packages
For Docking and Spin Label Modeling:

- MDAnalysis
- Acpype (https://github.com/alanwilter/acpype)
- RDKit
- Numpy
- ChiLife (https://github.com/StollLab/chiLife)
- SciPy
- Scikit-learn (SkLearn)

For Analysis of Results:
- Matplotlib
- Pandas
- PyMOL
