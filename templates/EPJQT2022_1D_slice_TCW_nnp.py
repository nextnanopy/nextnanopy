# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 16:04:36 2021

@author: kemal.oeztas
"""

import nextnanopy as nn
from nextnanopy.utils.misc import mkdir_if_not_exist
import os
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.constants import m_e, hbar

device_length = 600e9 #  x nm = x e9 meters

effective_mass = 0.067 # GaAs

E_meV  = 9.2e-3 # fixed electron energy

#Conversion from eV to Joule
E = E_meV * 1.6e-19

software = 'nextnano++' # Specify software product here!
software_short = '_nnp'

folder_input = r'C:\Users\kemal.oeztas\nextnanopy\input files\deploy'

folder_output        = nn.config.config[software]['outputdirectory'] # Define output folders. If they do not exist, they are created.
folder_output_python = os.path.join(folder_output, r'nextnanopy')
mkdir_if_not_exist(folder_output)
mkdir_if_not_exist(folder_output_python)

my_input_file_no_extension_nnp = r'EPJQT2022_2D_TCW_nnp'

FileExtension = '.in'  # for nextnano++ and nextnano3
my_input_file_no_extension = my_input_file_no_extension_nnp
my_input_file = my_input_file_no_extension+FileExtension

print("starting nextnano...")
input_file_name = os.path.join(folder_input, my_input_file)
input_file = nn.InputFile(input_file_name)

print(f"List of variables: {input_file.variables}")
for var in input_file.variables.values():
    print(f'{var.text}')

SweepVariable = 'tunnel_barrier_height'
comment_original = input_file.variables[SweepVariable].comment

SweepValues = [i*i for i in np.linspace(0.00, 1.00, 41)]

fixed_energy = 0.0092

dfV=[]
df_cbV=[]
SweepVariableStringV=[]
transmission_13_at_fixed_energy=[]
transmission_14_at_fixed_energy=[]

for x in [str(x) for x in SweepValues]:
    
    dt_string = 'TCW600nm'
    input_file.set_variable(SweepVariable, value=x, comment='<= PYTHON <=' + comment_original)
    
    for var in input_file.variables.values():
        print(var.text)      # --> better method to preview
    
    SweepVariableString = SweepVariable + '=' + x
    SweepVariableStringV.append(SweepVariableString)
    
    input_file_name_variable = my_input_file_no_extension + '; ' + SweepVariableString + '; @' + dt_string
    #input_file_name_variable = my_input_file_no_extension + '; ' + SweepVariableString
    my_input_file_new = os.path.join(folder_output, input_file_name_variable + FileExtension)
    print(my_input_file_new)
    
    input_file.save(my_input_file_new, overwrite=True, automkdir=True)
    
    input_file.execute() # Execute nextnano software. Put line into comment if you only want to to post-processing of results
    
    file    = os.path.join(folder_output,input_file_name_variable + r'\bias_00000' + r'\transmission_device_Gamma1.dat') 
    
    df    = nn.DataFile(file, product=software)
    dfV.append(df)
    
    transmission_13_at_fixed_energy_x = df.variables['1->3'].value[int((fixed_energy - input_file.variables['E_min'].value)/input_file.variables['delta_energy'].value) + 1]
    transmission_13_at_fixed_energy.append(transmission_13_at_fixed_energy_x)
    transmission_14_at_fixed_energy_x = df.variables['1->4'].value[int((fixed_energy - input_file.variables['E_min'].value)/input_file.variables['delta_energy'].value) + 1]
    transmission_14_at_fixed_energy.append(transmission_14_at_fixed_energy_x)
    print("Read in file:")
    print("current datafile: ",file)
    print(f"List of coordinates in the current datafile: {df.coords}")
    print(f"List of variables in the current datafile: {df.variables}")


my_input_file_no_extension_nnp = r'EPJQT2022_1D_slice_TCW_nnp'

my_input_file_no_extension = my_input_file_no_extension_nnp
my_input_file = my_input_file_no_extension+FileExtension

print("starting nextnano...")
input_file_name = os.path.join(folder_input, my_input_file)
input_file = nn.InputFile(input_file_name)

print(f"List of variables: {input_file.variables}")
for var in input_file.variables.values():
    print(f'{var.text}') # --> better method to preview
    
SweepVariable = 'tunnel_barrier_height'
comment_original = input_file.variables[SweepVariable].comment

SweepValues2 = [i**3 for i in np.linspace(0.18, 1.00, 41)]

dfV=[]
df_cbV=[]
SweepVariableStringV=[]

E_s = []
E_a = []
value_list = []
delta_k_list = []
scaling_factor = 44

for x in [str(x) for x in SweepValues2]:
    
    input_file.set_variable(SweepVariable, value=x, comment='<= PYTHON <=' + comment_original)
    
    SweepVariableString = SweepVariable + '=' + x
    SweepVariableStringV.append(SweepVariableString)
    
    input_file_name_variable = my_input_file_no_extension + '; ' + SweepVariableString    
    my_input_file_new = os.path.join(folder_output, input_file_name_variable + FileExtension)
    print(my_input_file_new)
    
    input_file.save(my_input_file_new, overwrite=True, automkdir=True)
    input_file.execute() # Execute nextnano software. Put line into comment if you only want to to post-processing of results
    file    = os.path.join(folder_output,input_file_name_variable + r'\bias_00000\Quantum' + r'\energy_spectrum_cbr_Gamma_00000.dat') 
    
    df    = nn.DataFile(file, product=software)
    dfV.append(df)
    
    E_s_x = df.variables['Energy'].value[0] 
    E_a_x = df.variables['Energy'].value[1] 
    
    E_s_j = E_s_x * 1.6e-19
    E_a_j = E_a_x * 1.6e-19
    
    delta_k = math.sqrt((2*effective_mass*m_e*(E-E_s_j))/hbar) - math.sqrt((2*effective_mass*m_e*(E-E_a_j))/hbar)
    
    delta_k_list.append(delta_k)
    
    value = math.cos(delta_k*device_length/scaling_factor)**2  # add **2 to square
  
    value_list.append(value)
    
fig, ax = plt.subplots(1)
ax.plot(SweepValues2, value_list, 'c.') 
ax.plot(SweepValues2, [1-x for x in value_list], 'g.')    
   
transmission13plus14 = [a + b for a, b in zip(transmission_13_at_fixed_energy, transmission_14_at_fixed_energy)]

ax.plot(SweepValues, transmission_13_at_fixed_energy, 'c-', label='1->3')
ax.plot(SweepValues, transmission_14_at_fixed_energy, 'g-', label='1->4')

ax.set_xlim(-0.00,1.0)
ax.set_ylim(0.0,1.0)
ax.set_xlabel('Tunneling barrier $V_{\mathrm{T}}$ (eV)', fontsize=14)
ax.set_ylabel('Transmission', fontsize=14)
ax.set_xticks(np.arange(0, 1.1, 0.1))

#fig.savefig('dotsandlines' + '.png', dpi=500, bbox_inches='tight',pad_inches = 0, transparent=True )

print('Done nextnanopy.')  
