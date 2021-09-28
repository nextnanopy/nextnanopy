import sys,os
import nextnanopy as nn
import numpy as np
import pathlib

#+++++++++++++++++++++++++++++++++++++++++++++++++
# Input file is located on Github
#+++++++++++++++++++++++++++++++++++++++++++++++++
InputFolder = os.path.join(pathlib.Path(__file__).parent.resolve(), r'input files')
filename = r'sweep_example.in'


#+++++++++++++++++++++++++++++++++++++++++++++++++
# Specify start value, end value, number of points
#+++++++++++++++++++++++++++++++++++++++++++++++++
SweepVariable1 = 'ALLOY'   # Al content in AlGaAs layer
alloyX_start  = 0.2   
alloyX_end    = 1.0
alloyX_points = 2

SweepVariable2 = 'SIZE'    # thickness of AlGaAs layer (nm)
thickness_start = 3.0
thickness_end   = 10.0
thickness_points= 3



#%%
ListOfValues_alloyX = np.linspace(alloyX_start, alloyX_end, alloyX_points)
ListOfValues_thickness = np.linspace(thickness_start, thickness_end, thickness_points)
InputPath = os.path.join(InputFolder, filename)
sweep = nn.Sweep({f'{SweepVariable1}':ListOfValues_alloyX, f'{SweepVariable2}':ListOfValues_thickness}, InputPath)
sweep.save_sweep()
sweep.execute_sweep(delete_input_files=True, overwrite=True)   # overwrite=True overwrites previous outputs with the same name