import nextnanopy as nn
from nextnanopy.utils.misc import mkdir_if_not_exist
import sys,os
#import numpy as np
import matplotlib.pyplot as plt

# config file is stored in C:\Users\<User>\.nextnanopy-config (home directory)

#++++++++++++++++++++++++++++++++++++++++++++++
# Specify output image format
#++++++++++++++++++++++++++++++++++++++++++++++
#FigFormat = '.pdf'
# FigFormat = '.svg'
FigFormat = '.jpg'
#FigFormat = '.png'


#++++++++++++++++++++++++++++++++++++++++++++++
# Specify input file folder  
#++++++++++++++++++++++++++++++++++++++++++++++
# nextnano++ examples
#input_folder = r'C:\Program Files\nextnano\2021_12_12\Sample files\nextnano++ sample files'
input_folder = r'C:\Program Files\nextnano\2021_12_12\Sample files\nextnano++ sample files\Quantum Mechanics examples'
# nextnano3 examples
# input_folder = r'C:\Program Files\nextnano\2021_09_03\Sample files\nextnano3 sample files\Quantum Mechanics examples'
# nextnano.NEGF examples
# input_folder = r'D:\nextnano.NEGF\nextnanoNEGF_2020_11_16\nextnano.NEGF sample files'
# nextnano.MSB examples
# input_folder = r'D:\nextnano.MSB\nextnano.MSB_2017_12_20\nextnano\2017_12_20\nextnano.MSB sample files'


#++++++++++++++++++++++++++++++++++++++++++++++
# Specify input file WITH file extension .in or .xml
#++++++++++++++++++++++++++++++++++++++++++++++
#filename = r'Jogai_AlGaNGaN_FET_JAP2003_GaNcap_Fig6Fig5_1D_nnp.in'
#filename = r'Jogai_AlGaNGaN_FET_JAP2003_GaNcap_Fig6Fig5_1D_nn3.in'
#filename = r'2D_CBR_MamaluySabathilJAP2003_AharonovBohm.in'
#filename = r'2D_CBR_square.in'
filename = r'Transmission_Double_Barrier_1D_nnp.in'
# filename = r'Transmission_Double_Barrier_1D_nn3.in'


#++++++++++++++++++++++++++++++++++++++++++++++
# Specify which variable, in which range to sweep
#++++++++++++++++++++++++++++++++++++++++++++++
#SweepVariable = 'ThicknessAlGaN'
#SweepVariable = 'ThicknessGaNcap'
SweepVariable = 'Barrier_Width'
#ListOfValues = ["10.0"]
#ListOfValues = ["10.0", "15.0", "20.0"]
#ListOfValues = ["1","2","3","4","5","7","9","11","12","13","14","15","17","20","25","30"]
#ListOfValues = ["1","3","7","12","20","30"]
ListOfValues = ["2.0", "4.0", "10.0"]



#%%
# define a function to detect which software to execute
def detect_software(folder_path, filename):
    if not '.' in filename:
        print('ERROR: Please specify input file with extension (.in or .xml)')
        sys.exit()

    InputPath = os.path.join(folder_path, filename)
    with open(InputPath,'r') as file:
        for line in file:
            if 'simulation-flow-control' in line:
                software = 'nextnano3'
                software_short = '_nn3'
                FileExtension = '.in'
                break
            elif 'run{' in line:
                software = 'nextnano++'
                software_short = '_nnp'
                FileExtension = '.in'
                break
            elif '<nextnano.NEGF' in line:
                software = 'nextnano.NEGF'
                software_short = '_nnNEGF'
                FileExtension = '.xml'
                break            
            elif '<nextnano.MSB' in line:
                software = 'nextnano.MSB'
                software_short = '_nnMSB'
                FileExtension = '.xml'
                
    if not software:   # if the variable is empty
        print('ERROR: Software cannot be detected! Please check your input file.')
        sys.exit()
    else: 
        print('Software detected: ', software)
    
    return software, software_short, FileExtension

# detect software based on input file
software, software_short, FileExtension = detect_software(input_folder, filename)

# Define output folders. If they do not exist, they are created.
folder_output        = nn.config.config[software]['outputdirectory']
folder_output_python = os.path.join(folder_output, r'nextnanopy')
mkdir_if_not_exist(folder_output_python)

# plt.ion() # interactive mode
print("starting nextnano...")
input_path = os.path.join(input_folder, filename)
input_file = nn.InputFile(input_path)

print(f"List of variables: {input_file.variables}")
for var in input_file.variables.values():
  # print(f'${var.name} = {var.value} ! {var.comment}')
    print(f'{var.text}') # --> better method to preview

comment_original = input_file.variables[SweepVariable].comment

filename_no_extension = filename.replace(FileExtension, '')
dfV=[]
df_cbV=[]
SweepVariableStringV=[]
for x in ListOfValues:

  input_file.set_variable(SweepVariable, value=x, comment='<= PYTHON <= ' + comment_original)

  for var in input_file.variables.values():
    # print(f'${var.name} = {var.value} ! {var.comment}')
    # print(f'{var.text}') # --> better method to preview
      print(var.text)      # --> better method to preview

  SweepVariableString = SweepVariable + '_' + x
  SweepVariableStringV.append(SweepVariableString)

  input_file_name_variable = filename_no_extension + '_' + SweepVariableString

  my_input_file_new = os.path.join(folder_output, input_file_name_variable+FileExtension)
  print(my_input_file_new)

  input_file.save(my_input_file_new, overwrite=True, automkdir=True)

  print('')  
  print('=====================================')  
  ############################
  # Execute nextnano software
  ############################
  input_file.execute() # Put line into comment if you only want to to post-processing of results
  print('=====================================')  

  #plotL = bool(0) # false
  plotL = bool(1) # true

  if(plotL):
  
    print('=====================================')  
    print('Now generate plots in output folder')  
    print(folder_output)  
    print('=====================================')  

#++++++++++++++++++++++++++++++++++++++++++++++
# Adjust path to output files if necessary
#++++++++++++++++++++++++++++++++++++++++++++++
#===========================
    if(software=="nextnano++"):
        file    = os.path.join(folder_output, input_file_name_variable+r'\bias_00000'+r'\transmission_cbr_Gamma1.dat') 
        file_cb = os.path.join(folder_output, input_file_name_variable+r'\bias_00000'+r'\bandedge_Gamma.dat') 
    elif(software=="nextnano3"):
        file    = os.path.join(folder_output, input_file_name_variable+r'\Results'+r'\Transmission_cb_sg1_deg1.dat') 
      # file    = os.path.join(folder_output, input_file_name_variable+r'\band_structure'+r'\BandEdges_A000.dat') 
        file_cb = os.path.join(folder_output, input_file_name_variable+r'\Results'+r'\cb_Gamma.dat') 
#===========================
    df    = nn.DataFile(file, product=software)
    dfV.append(df)

    # Conduction band edge
    print("Read in file:")
    print(file_cb)
    df_cb = nn.DataFile(file_cb, product=software)
    df_cbV.append(df_cb)

    print("current datafile: ",file)
    print(f"List of coordinates in the current datafile: {df.coords}")
    print(f"List of variables in the current datafile: {df.variables}")

    print("current datafile: ",file_cb)
    print(f"List of coordinates in the current datafile: {df_cb.coords}")
    print(f"List of variables in the current datafile: {df_cb.variables}")

    fig, ax = plt.subplots(1)
    if(software=="nextnano++"):  ax.plot(df.variables[0].value, df.variables[2].value, label=SweepVariableString)
    elif(software=="nextnano3"): ax.plot(df.variables[0].value, df.variables[1].value, label=SweepVariableString)

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
    fig.savefig(file + FigFormat)

#++++++++++++++++++++++++++++++++++++++++++++++
# Adjust path to output files  if necessary
# 2D plot from nextnano3
#++++++++++++++++++++++++++++++++++++++++++++++
    if(software=="nextnano3"):
     #  file = os.path.join(folder_output, input_file_name_variable+r'\Schroedinger_1band'+r'\2Dcb1_qc1_sg1_deg1_psi_squared_ev001.fld') 
        file = os.path.join(folder_output, input_file_name_variable+r'\Results'+r'\LocalDOS_sg1_deg1.fld') 
      # file = os.path.join(folder_output, input_file_name_variable+r'\Results'+r'\LocalDOS_sg1_deg1.vtr') 
        datafile_2d = nn.DataFile(file, product=software)
        print("current datafile: ", file)
        print(f"List of coordinates in the current datafile: {datafile_2d.coords}")
        print(f"List of variables in the current datafile: {datafile_2d.variables}")
    
        x=datafile_2d.coords['x']
        y=datafile_2d.coords['y']
      # z=datafile_2d.variables['psi_squared']
        z=datafile_2d.variables[0]

        fig, ax = plt.subplots(1)
        pcolor = ax.pcolormesh(x.value, y.value, z.value.T)
        cbar = fig.colorbar(pcolor)
        cbar.set_label(f"{z.name} ({z.unit})")
        ax.plot(df_cb.coords[0].value,df_cb.variables[0].value, label=SweepVariableString,
                color='white', linestyle='-')

     #   ax.plot(df_cb.coords['position'].value,df_cb.variables[1].value,color='yellow')
    #    for i in range(2,len(ws)):
    #        ax.plot(df_cb.coords['position'].value,ws[i],color='yellow')
    
        ax.set_xlabel(f"{x.name} ({x.unit})")
        ax.set_ylabel(f"{y.name} ({y.unit})")
        ax.set_title('Local density of states')
        fig.tight_layout()
      # plt.show()
        fig.savefig(file + FigFormat)

fig, ax = plt.subplots(1)

for i,j in zip(dfV, SweepVariableStringV):
    if(software=="nextnano++"):  ax.plot(i.variables[0].value, i.variables[2].value, label=j)
    elif(software=="nextnano3"): ax.plot(i.variables[0].value, i.variables[1].value, label=j)

ax.set_xlabel(f"{df.variables[0].name} ({df.variables[0].unit})")
ax.set_ylabel(f"{df.variables[1].name} ({df.variables[1].unit})")
ax.set_title('Transmission')
ax.legend()
fig.tight_layout()
#plt.show()
fig.savefig(os.path.join(folder_output_python, 'Transmission'+'_'+SweepVariable+software_short+FigFormat))

print('=====================================')  
print('Done nextnanopy.')  
print('=====================================')  
