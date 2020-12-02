import nextnanopy as nn
from nextnanopy.utils.misc import mkdir_if_not_exist
import sys,os
#import numpy as np
import matplotlib.pyplot as plt

import config_nextnano     # This should be your default configuration.
#import config_nextnano_temp # This could be a modified configuration file.
# config file is stored in C:\Users\<User>\.nextnanopy-config

#++++++++++++++++++++++++++++++++++++++++++++++
# These lines have to be adjusted by the user.  
#++++++++++++++++++++++++++++++++++++++++++++++
#================================
# Specify software product here!
#================================
software = 'nextnano++'
#software = 'nextnano3'
#software = 'nextnano.NEGF'
#software = 'nextnano.MSB'
#===========================

folder_examples_nnp = r'C:\Program Files\nextnano\2020_10_16\Sample files\nextnano++ sample files'
folder_examples_nn3 = r'C:\Program Files\nextnano\2020_10_16\Sample files\nextnano3 sample files'
folder_examples_nnNEGF = r'D:\nextnano.NEGF\nextnanoNEGF_2020_11_16\nextnano.NEGF sample files'
folder_examples_nnMSB = r'D:\nextnano.MSB\nextnano.MSB_2017_12_20\nextnano\2017_12_20\nextnano.MSB sample files'

#===========================
if(software=="nextnano++"):
    subfolder = ''
  # subfolder = r'\Quantum Mechanics examples'
elif(software=="nextnano3"):
    subfolder = ''
  # subfolder = r'\Quantum Mechanics examples'
elif(software=="nextnano.NEGF"):
    subfolder = ''
elif(software=="nextnano.MSB"):
    subfolder = ''
#===========================

software_short_nnp    = '_nnp'
software_short_nn3    = '_nn3'
software_short_nnNEGF = '_nnNEGF'
software_short_nnMSB  = '_nnMSB'

#===========================
if(software=="nextnano++"):
    folder_examples = folder_examples_nnp + subfolder   # nextnano++
elif(software=="nextnano3"):
    folder_examples = folder_examples_nn3 + subfolder   # nextnano3
elif(software=="nextnano.NEGF"):
    folder_examples = folder_examples_nnNEGF + subfolder # nextnano.NEGF
elif(software=="nextnano.MSB"):
    folder_examples = folder_examples_nnMSB + subfolder # nextnano.MSB
#===========================

#================================================================
# Define output folders. If they do not exist, they are created.
#================================================================
folder_output        = nn.config.config[software]['outputdirectory']
folder_output_python = os.path.join(folder_output,r'nextnanopy')
mkdir_if_not_exist(folder_output)
mkdir_if_not_exist(folder_output_python)

#--------------------------------------------------------
# Specify input file without file extension '.in'/.'xml'
#--------------------------------------------------------
my_input_file_no_extension_nnp = r'Jogai_AlGaNGaN_FET_JAP2003_GaNcap_Fig6Fig5_1D_nnp'
my_input_file_no_extension_nn3 = r'Jogai_AlGaNGaN_FET_JAP2003_GaNcap_Fig6Fig5_1D_nn3'
#my_input_file_no_extension_nnp = r'Transmission_Double_Barrier_1D_nnp'
#my_input_file_no_extension_nn3 = r'Transmission_Double_Barrier_1D_nn3'
my_input_file_no_extension_nnNEGF = r'THz_QCL_GaAs_AlGaAs_Fathololoumi_OptExpress2012_10K-FAST'
my_input_file_no_extension_nnMSB = r'1D_Transmission_DoubleBarrier_CBR_paper_MSB'

#===========================
if(software=="nextnano++"):
    my_input_file_no_extension = my_input_file_no_extension_nnp
    software_short = software_short_nnp
elif(software=="nextnano3"):
    my_input_file_no_extension = my_input_file_no_extension_nn3
    software_short = software_short_nn3
elif(software=="nextnano.NEGF"):
    my_input_file_no_extension = my_input_file_no_extension_nnNEGF
    software_short = software_short_nnNEGF
elif(software=="nextnano.MSB"):
    my_input_file_no_extension = my_input_file_no_extension_nnMSB
    software_short = software_short_nnMSB
#===========================

if(software=="nextnano.NEGF" or software=="nextnano.MSB"):
    FileExtension = '.xml' # for nextnano.NEGF and nextnano.MSB
else:
    FileExtension = '.in'  # for nextnano++ and nextnano3

my_input_file = my_input_file_no_extension+FileExtension

# plt.ion() # interactive mode

print(f"starting nextnano...")
input_file_name = os.path.join(folder_examples,my_input_file)
input_file = nn.InputFile(input_file_name)

#++++++++++++++++++++++++++++++++++++++++++++++
# These lines have to be adjusted by the user.  
#++++++++++++++++++++++++++++++++++++++++++++++
print(f"List of variables: {input_file.variables}")
for var in input_file.variables.values():
  # print(f'${var.name} = {var.value} ! {var.comment}')
    print(f'{var.text}') # --> better method to preview

#SweepVariable = 'ThicknessAlGaN'
SweepVariable = 'ThicknessGaNcap'

comment_original = input_file.variables[SweepVariable].comment
#ListOfValues = ["10.0"]
#ListOfValues = ["10.0", "15.0", "20.0"]
#ListOfValues = ["1","2","3","4","5","7","9","11","12","13","14","15","17","20","25","30"]
ListOfValues = ["1","3","7","12","20","30"]
dfV=[]
df_cbV=[]
SweepVariableStringV=[]
for x in ListOfValues:

  input_file.set_variable(SweepVariable, value=x, comment='<= PYTHON <= ' + comment_original)

  for var in input_file.variables.values():
    # print(f'${var.name} = {var.value} ! {var.comment}')
    # print(f'{var.text}') # --> better method to preview
      print(var.text)      # --> better method to preview

  SweepVariableString = SweepVariable+'_'+x
  SweepVariableStringV.append(SweepVariableString)

  input_file_name_variable = my_input_file_no_extension+'_'+SweepVariableString

  my_input_file_new = os.path.join(folder_output,input_file_name_variable+FileExtension)
  print(my_input_file_new)

  input_file.save(my_input_file_new,overwrite=True,automkdir=True)

  print(f'')  
  print(f'=====================================')  
  ############################
  # Execute nextnano software
  ############################
  input_file.execute() # Put line into comment if you only want to to post-processing of results
  print(f'=====================================')  

# plotL = bool(0) # false
  plotL = bool(1) # true

  if(plotL):
  
    print(f'=====================================')  
    print(f'Now generate plots in output folder')  
    print(folder_output)  
    print(f'=====================================')  

#++++++++++++++++++++++++++++++++++++++++++++++
# These lines have to be adjusted by the user.  
#++++++++++++++++++++++++++++++++++++++++++++++
#===========================
    if(software=="nextnano++"):
        file = os.path.join(folder_output,input_file_name_variable+r'\bias_000_000'+r'\bandedges.dat') 
        my_input_file_no_extension = my_input_file_no_extension_nnp
    elif(software=="nextnano3"):
        file = os.path.join(folder_output,input_file_name_variable+r'\band_structure'+r'\BandEdges.dat') 
#===========================
    df = nn.DataFile(file,product=software)
    dfV.append(df)

    fig, ax = plt.subplots(1)
#++++++++++++++++++++++++++++++++++++++++++++++
# These lines have to be adjusted by the user.  
#++++++++++++++++++++++++++++++++++++++++++++++
#===========================
    if(software=="nextnano++"):
        ax.plot(df.coords['x'].value,df.variables['Gamma'].value,label='Gamma')
        ax.plot(df.coords['x'].value,df.variables['electron_Fermi_level'].value, label='FermiLevel_el')

        ax.set_xlabel(f"{df.coords['x'].name} {df.coords['x'].unit}")
        ax.set_ylabel(f"Energy {df.variables['Gamma'].unit}")
    elif(software=="nextnano3"):
        ax.plot(df.coords['position'].value,df.variables['Gamma_bandedge'].value,label='Gamma')
        ax.plot(df.coords['position'].value,df.variables['FermiLevel_el'].value, label='FermiLevel_el')

        ax.set_xlabel(f"{df.coords['position'].name} {df.coords['position'].unit}")
        ax.set_ylabel(f"Energy {df.variables['Gamma_bandedge'].unit}")
    ax.legend()
    fig.tight_layout()
  # plt.show()
    fig.savefig(file+'.jpg')
  
print(f'=====================================')  
print(f'Done nextnanopy.')  
print(f'=====================================')  
