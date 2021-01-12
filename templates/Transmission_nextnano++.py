import nextnanopy as nn
from nextnanopy.utils.misc import mkdir_if_not_exist
import sys,os
#import numpy as np
import matplotlib.pyplot as plt

#import config_nextnano     # This should be your default configuration.
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

folder_examples_nnp    = r'C:\Program Files\nextnano\2020_12_09\Sample files\nextnano++ sample files'
folder_examples_nn3    = r'C:\Program Files\nextnano\2020_12_09\Sample files\nextnano3 sample files'
folder_examples_nnNEGF = r'D:\nextnano.NEGF\nextnanoNEGF_2020_11_16\nextnano.NEGF sample files'
folder_examples_nnMSB  = r'D:\nextnano.MSB\nextnano.MSB_2017_12_20\nextnano\2017_12_20\nextnano.MSB sample files'

#++++++++++++++++++++++++++++++++++++++++++++++
# These lines have to be adjusted by the user.  
#++++++++++++++++++++++++++++++++++++++++++++++
#folder_examples_nn3 = r'N:\users\nextnano\nextnano GmbH - Tutorials\Tutorials\2D The CBR method (Transmission)'
#===========================
if(software=="nextnano++"):
  # subfolder = ''
    subfolder = r'\Quantum Mechanics examples'
elif(software=="nextnano3"):
  # subfolder = ''
    subfolder = r'\Quantum Mechanics examples'
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
#my_input_file_no_extension_nnp = r'Jogai_AlGaNGaN_FET_JAP2003_GaNcap_Fig6Fig5_1D_nnp'
#my_input_file_no_extension_nn3 = r'Jogai_AlGaNGaN_FET_JAP2003_GaNcap_Fig6Fig5_1D_nn3'
#my_input_file_no_extension_nn3 = r'2D_CBR_MamaluySabathilJAP2003_AharonovBohm'
#my_input_file_no_extension_nn3 = r'2D_CBR_square'
my_input_file_no_extension_nnp = r'Transmission_Double_Barrier_1D_nnp'
my_input_file_no_extension_nn3 = r'Transmission_Double_Barrier_1D_nn3'
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
#SweepVariable = 'ThicknessGaNcap'
SweepVariable = 'Barrier_Width'

comment_original = input_file.variables[SweepVariable].comment
#ListOfValues = ["10.0"]
#ListOfValues = ["10.0", "15.0", "20.0"]
#ListOfValues = ["1","2","3","4","5","7","9","11","12","13","14","15","17","20","25","30"]
#ListOfValues = ["1","3","7","12","20","30"]
ListOfValues = ["2.0", "4.0", "10.0"]

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

  #plotL = bool(0) # false
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
        file    = os.path.join(folder_output,input_file_name_variable+r'\bias_000_000'+r'\transmission_cbr_Gamma1.dat') 
        file_cb = os.path.join(folder_output,input_file_name_variable+r'\bias_000_000'+r'\bandedge_Gamma.dat') 
    elif(software=="nextnano3"):
        file    = os.path.join(folder_output,input_file_name_variable+r'\Results'+r'\Transmission_cb_sg1_deg1.dat') 
      # file    = os.path.join(folder_output,input_file_name_variable+r'\band_structure'+r'\BandEdges_A000.dat') 
        file_cb = os.path.join(folder_output,input_file_name_variable+r'\Results'+r'\cb_Gamma.dat') 
#===========================
    df    = nn.DataFile(file,product=software)
    dfV.append(df)

    #===========================
    # Conduction band edge
    #===========================
    print(f"Read in file:")
    print(file_cb)
    df_cb = nn.DataFile(file_cb,product=software)
    df_cbV.append(df_cb)

    print(f"current datafile: ",file)
    print(f"List of coordinates in the current datafile: {df.coords}")
    print(f"List of variables in the current datafile: {df.variables}")

    print(f"current datafile: ",file_cb)
    print(f"List of coordinates in the current datafile: {df_cb.coords}")
    print(f"List of variables in the current datafile: {df_cb.variables}")
#   print(f"{df.coords['position'].unit}")

    fig, ax = plt.subplots(1)
    ax.plot(df.variables[0].value,df.variables[1].value,label=SweepVariableString)

#   ax.plot(df.coords['position'].value,df.variables['T_1_2'].value,label='Transmission')
#   ax.plot(df.variables['energy'].value,df.variables['T_1_2'].value,label='Transmission')
#   ax.plot(df.coords['position'].value,df.variables['FermiLevel_el'].value, label='FermiLevel_el')
#   ax.plot(df.coords['energy'].value,df.variables['Gamma_bandedge'].value,label='Gamma')

  #  ax.set_xlabel(f"{df.coords['position'].name} {df.coords['position'].unit}")
  #  ax.set_ylabel(f"Energy {df.variables['T_1_2'].unit}")

    ax.set_xlabel(f"{df.variables[0].name} ({df.variables[0].unit})")
    ax.set_ylabel(f"{df.variables[1].name} ({df.variables[1].unit})")
    ax.set_title('Transmission')
    ax.legend()
    fig.tight_layout()
  # plt.show()
    fig.savefig(file+'.jpg')

#++++++++++++++++++++++++++++++++++++++++++++++
# These lines have to be adjusted by the user.  
# 2D plot
#++++++++++++++++++++++++++++++++++++++++++++++
    if(software=="nextnano3"):
     #  file = os.path.join(folder_output,input_file_name_variable+r'\Schroedinger_1band'+r'\2Dcb1_qc1_sg1_deg1_psi_squared_ev001.fld') 
        file = os.path.join(folder_output,input_file_name_variable+r'\Results'+r'\LocalDOS_sg1_deg1.fld') 
      # file = os.path.join(folder_output,input_file_name_variable+r'\Results'+r'\LocalDOS_sg1_deg1.vtr') 
        datafile_2d = nn.DataFile(file,product=software)
        print(f"current datafile: ",file)
        print(f"List of coordinates in the current datafile: {datafile_2d.coords}")
        print(f"List of variables in the current datafile: {datafile_2d.variables}")
    
        x=datafile_2d.coords['x']
        y=datafile_2d.coords['y']
      # z=datafile_2d.variables['psi_squared']
        z=datafile_2d.variables[0]

        fig, ax = plt.subplots(1)
        pcolor = ax.pcolormesh(x.value,y.value,z.value.T)
        cbar = fig.colorbar(pcolor)
        cbar.set_label(f"{z.name} ({z.unit})")
        ax.plot(df_cb.coords[0].value,df_cb.variables[0].value,label=SweepVariableString,
                color='white', linestyle='-')

     #   ax.plot(df_cb.coords['position'].value,df_cb.variables[1].value,color='yellow')
    #    for i in range(2,len(ws)):
    #        ax.plot(df_cb.coords['position'].value,ws[i],color='yellow')
    
        ax.set_xlabel(f"{x.name} ({x.unit})")
        ax.set_ylabel(f"{y.name} ({y.unit})")
        ax.set_title('Local density of states')
        fig.tight_layout()
      # plt.show()
        fig.savefig(file+'.jpg')

fig, ax = plt.subplots(1)

for i,j in zip(dfV,SweepVariableStringV):
    ax.plot(i.variables[0].value,i.variables[1].value,label=j)

ax.set_xlabel(f"{df.variables[0].name} ({df.variables[0].unit})")
ax.set_ylabel(f"{df.variables[1].name} ({df.variables[1].unit})")
ax.set_title('Transmission')
ax.legend()
fig.tight_layout()
#plt.show()
fig.savefig(os.path.join(folder_output_python,'Transmission'+'_'+SweepVariable+software_short+'.jpg'))

print(f'=====================================')  
print(f'Done nextnanopy.')  
print(f'=====================================')  
