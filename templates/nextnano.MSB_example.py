import nextnanopy as nn
import sys,os
#import numpy as np
import matplotlib.pyplot as plt

import config_nextnano
# config file is stored in C:\Users\<User>\.nextnanopy-config

#++++++++++++++++++++++++++++++++++++++++++++++
# These lines have to be adjusted by the user.  
#++++++++++++++++++++++++++++++++++++++++++++++
#================================
# Specify software product here!
#================================
#software = 'nextnano++'
#software = 'nextnano3'
#software = 'nextnano.NEGF'
software = 'nextnano.MSB'
#===========================

folder_examples_nnp = r'C:\Program Files\nextnano\2020_10_16\Sample files\nextnano++ sample files'
folder_examples_nn3 = r'C:\Program Files\nextnano\2020_10_16\Sample files\nextnano3 sample files'
folder_examples_nnNEGF = r'D:\nextnano.NEGF\nextnanoNEGF_2020_11_16\nextnano.NEGF sample files'
folder_examples_nnMSB = r'D:\nextnano.MSB\nextnano.MSB_2017_12_20\nextnano\2017_12_20\nextnano.MSB sample files'

#===========================
if(software=="nextnano++"):
    folder_examples = folder_examples_nnp # nextnano++
elif(software=="nextnano3"):
    folder_examples = folder_examples_nn3 # nextnano3
elif(software=="nextnano.NEGF"):
    folder_examples = folder_examples_nnNEGF # nextnano.NEGF
elif(software=="nextnano.MSB"):
    folder_examples = folder_examples_nnMSB # nextnano.MSB
#===========================

folder_output = os.path.join(nn.config.get(software,'outputdirectory'),r'nextnanopy')
#r'C:\D\nextnanopython_test\output'
print(f"Python output folder: ",folder_output)

#--------------------------------------------------------
# Specify input file without file extension '.in'/.'xml'
#--------------------------------------------------------
my_input_file_no_extension_nnp = r'Jogai_AlGaNGaN_FET_JAP2003_noGaNcap_Fig2Fig3_1D_nnp'
my_input_file_no_extension_nn3 = r'Jogai_AlGaNGaN_FET_JAP2003_noGaNcap_Fig2Fig3_1D_nn3'
my_input_file_no_extension_nnNEGF = r'THz_QCL_GaAs_AlGaAs_Fathololoumi_OptExpress2012_10K-FAST'
my_input_file_no_extension_nnMSB = r'1D_Transmission_DoubleBarrier_CBR_paper_MSB'
my_input_file_no_extension_nnMSB = r'1D_Transmission_DoubleBarrier_CBR_paper_MSB_test'

#===========================
if(software=="nextnano++"):
    my_input_file_no_extension = my_input_file_no_extension_nnp
elif(software=="nextnano3"):
    my_input_file_no_extension = my_input_file_no_extension_nn3
elif(software=="nextnano.NEGF"):
    my_input_file_no_extension = my_input_file_no_extension_nnNEGF
elif(software=="nextnano.MSB"):
    my_input_file_no_extension = my_input_file_no_extension_nnMSB
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

input_file_name_variable = my_input_file_no_extension

my_input_file_new = os.path.join(folder_output,input_file_name_variable+FileExtension)
print(f"input file:")
print(my_input_file_new)

input_file.save(my_input_file_new,overwrite=True,automkdir=True)
print(f'')  
print(f'=====================================')  
####################################
input_file.execute()
####################################

#plotL = bool(0) # false
plotL = bool(1) # true

if(plotL):
  
  print(f'=====================================')  
  print(f'Now generate plots...')  
  print(f'=====================================')  

  folder = nn.config.config[software]['outputdirectory']
  print(f"output folder:")
  print(folder)  
#++++++++++++++++++++++++++++++++++++++++++++++
# These lines have to be adjusted by the user.  
#++++++++++++++++++++++++++++++++++++++++++++++
#===========================
  if(software=="nextnano++"):
      print(f"nextnano++ not implemented!")
  elif(software=="nextnano3"):
      print(f"nextnano3 not implemented!")
  elif(software=="nextnano.NEGF"):

      folder_results = input_file_name_variable
      print(f"output folder_results:")
      print(folder_results)

      folder_total = os.path.join(folder,folder_results)
      print(f"output folder_total:")
      print(folder_total)

      folder_bias = folder_results+r'\2mV'
      print(f"output folder_bias:")
      print(folder_bias)

      folder_total_bias = os.path.join(folder,folder_bias)
      print(f"output folder_total_bias:")
      print(folder_total_bias)

      file_cb = folder_total_bias+r'\Conduction_BandEdge.dat'
  elif(software=="nextnano.MSB"):

      folder_results = input_file_name_variable+r'\BarrierThickness=2'
      print(f"output folder_results:")
      print(folder_results)

      folder_total = os.path.join(folder,folder_results)
      print(f"output folder_total:")
      print(folder_total)

      folder_bias = folder_results+r'\Source=0V, Drain=0V'
      print(f"output folder_bias:")
      print(folder_bias)

      folder_total_bias = os.path.join(folder,folder_bias)
      print(f"output folder_total_bias:")
      print(folder_total_bias)

      file_cb = folder_total_bias+r'\BandProfile'+r'\BandEdge_conduction.dat'
#===========================
# Conduction band edge
#===========================
  print(f"Read in file:")
  print(file_cb)
  df = nn.DataFile(file_cb,software)

  fig, ax = plt.subplots(1)
  ax.plot(df.coords['Position'].value,df.variables['Conduction Band Edge'].value,label='Conduction Band Edge')
  
  ax.set_xlabel(f"{df.coords['Position'].name} {df.coords['Position'].unit}")
  ax.set_ylabel(f"Energy {df.variables['Conduction Band Edge'].unit}")
  ax.legend()
  fig.tight_layout()
# plt.show()
  fig.savefig(file_cb+'.jpg')

  if(software=="nextnano++"):
      file_LDOS = ''
      file_Density = ''
      file_Current = ''
  elif(software=="nextnano3"):
      file_LDOS = ''
      file_Density = ''
      file_Current = ''
  elif(software=="nextnano.NEGF"):
      subfolder = '2D_plots'
      file_LDOS = 'DOS_energy_resolved.vtr'
      file_Density = 'CarrierDensity_energy_resolved.vtr'
      file_Current = 'CurrentDensity_energy_resolved.vtr'
  elif(software=="nextnano.MSB"):
      file_LDOS = 'DOS_position_resolved.vtr'
      file_Density = 'CarrierDensity_energy_resolved.vtr'
      file_Current = 'CurrentDensity_energy_resolved.vtr'

  folder2Dplots = os.path.join(folder,folder_bias)
  for i in range(3):
      if(i == 0):
          if(software=="nextnano.MSB"): subfolder = 'DOS'
          label = 'Local density of states LDOS(x,E)'
          file = file_LDOS
      elif(i == 1):
          if(software=="nextnano.MSB"): subfolder = 'CarrierDensity'
          label = 'Carrier density n(x,E)'
          file = file_Density
      elif(i == 2):
          if(software=="nextnano.MSB"): subfolder = 'CurrentDensity'
          label = 'Current density j(x,E)'
          file = file_Current

      vtr_folder = os.path.join(folder2Dplots,subfolder)
      vtr_file = os.path.join(vtr_folder,file)
      dff = nn.DataFile(vtr_file,product=software)
      cX = dff.coords['x'].value
      cY = dff.coords['y'].value
      cZ = dff.variables[0].value
      fD, a2D1 = plt.subplots()
      im1 = a2D1.pcolormesh(cX, cY, cZ, cmap='gnuplot')
      a2D1.plot(df.coords[0].value,df.variables[0].value,label='Conduction Band Edge',
              color='white', linestyle='-')
      a2D1.set_title(label)  
      filename = vtr_file+'.jpg'
      print(f'Saving file: ',filename)
      fD.savefig(filename)

    
print(f'=====================================')  
print(f'Done nextnanopy.')  
print(f'=====================================')  
