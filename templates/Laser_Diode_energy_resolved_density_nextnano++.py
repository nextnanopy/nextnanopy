import nextnanopy as nn
from nextnanopy.utils.misc import mkdir_if_not_exist
import sys,os
import numpy as np
import matplotlib.pyplot as plt

#import config_nextnano     # This should be your default configuration.
#import config_nextnano_temp # This could be a modified configuration file.
# config file is stored in C:\Users\<User>\.nextnanopy-config

#FigFormat = '.pdf'
FigFormat = '.svg'
#FigFormat = '.jpg'
#FigFormat = '.png'

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

folder_examples_nnp    = r'C:\Program Files\nextnano\2021_08_06\Sample files\nextnano++ sample files'
folder_examples_nn3    = r'C:\Program Files\nextnano\2021_08_06\Sample files\nextnano3 sample files'
folder_examples_nnNEGF = r'D:\nextnano.NEGF\nextnanoNEGF_2020_11_16\nextnano.NEGF sample files'
folder_examples_nnMSB  = r'D:\nextnano.MSB\nextnano.MSB_2017_12_20\nextnano\2017_12_20\nextnano.MSB sample files'

#++++++++++++++++++++++++++++++++++++++++++++++
# These lines have to be adjusted by the user.  
#++++++++++++++++++++++++++++++++++++++++++++++
#folder_examples_nn3 = r'N:\users\nextnano\nextnano GmbH - Tutorials\Tutorials\2D The CBR method (Transmission)'
#===========================
if(software=="nextnano++"):
   subfolder = ''
  #  subfolder = r'\Quantum Mechanics examples'
elif(software=="nextnano3"):
   subfolder = ''
  #  subfolder = r'\Quantum Mechanics examples'
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
    software_short = software_short_nnp
elif(software=="nextnano3"):
    software_short = software_short_nn3
elif(software=="nextnano.NEGF"):
    software_short = software_short_nnNEGF
elif(software=="nextnano.MSB"):
    software_short = software_short_nnMSB
#===========================

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
my_input_file_no_extension_nnp = r'LaserDiode_InGaAs_1D_qm_nnp_nnmat_AvsAscii_one_file'
my_input_file_no_extension_nn3 = r'Transmission_Double_Barrier_1D_nn3'
my_input_file_no_extension_nnNEGF = r'THz_QCL_GaAs_AlGaAs_Fathololoumi_OptExpress2012_10K-FAST'
my_input_file_no_extension_nnMSB = r'1D_Transmission_DoubleBarrier_CBR_paper_MSB'

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
input_file = nn.InputFile(r'C:\Users\naoki.mitsui\Documents\nextnano\My input files\laser_diode_tutorial\LaserDiode_InGaAs_1D_qm_nnp_nnmat_AvsAscii_one_file.in')



print(f'')  
print(f'=====================================')  
############################
# Execute nextnano software
############################
# input_file.execute() # Put line into comment if you only want to to post-processing of results
print(f'=====================================')  





############################
# plot energy-resolved density + conduction bandedge (cb)
############################
ListOfValues = ['00000', '00001', '00002', '00003', '00004', '00005', '00006', '00007', '00008', '00009', '00010']
#ListOfValues = ['00001', '00008']
bias = 0
count = 0
inner_count = 0

fig_several = plt.figure()

for i in ListOfValues:
    bias = round(bias, 1)
    #===========================
    # Conduction and valence band edge
    #===========================
    file_be = os.path.join(folder_output,my_input_file_no_extension+r'\bias_'+i+r'\bandedges.dat') 
    
    print(f"Read in file:")
    print(file_be)
    df_be = nn.DataFile(file_be,product=software)

    #===========================
    # Energy-resolved electron density
    #===========================
    file_elec = os.path.join(folder_output,my_input_file_no_extension+r'\bias_'+i+r'\electron_density_vs_energy.fld') 
    #  file = os.path.join(folder_output,input_file_name_variable+r'\Results'+r'\LocalDOS_sg1_deg1.vtr')
    # Caution! Specify "format2D=AvsAscii_one_file" in the input file. Otherwise this line causes error due to the binary data reading.
    datafile_2d = nn.DataFile(file_elec,product=software)
    
    x=datafile_2d.coords['x']
    y=datafile_2d.coords['y']
    z_elec=datafile_2d.variables[0]
    
    fig, ax = plt.subplots(1)
    pcolor = ax.pcolormesh(x.value,y.value,z_elec.value.T)
    cbar = fig.colorbar(pcolor)
    cbar.set_label('Electron density [cm$^{-3}$eV$^{-1}$]')
    # conduction bandedge plot
    ax.plot(df_be.coords[0].value,df_be.variables[0].value, color='white', linestyle='-')
    # HH valence bandedge plot
    ax.plot(df_be.coords[0].value,df_be.variables[1].value, color='white', linestyle='-')
    # electron Fermi level plot
    ax.plot(df_be.coords[0].value,df_be.variables[4].value, color='red',  linestyle='dotted', linewidth=1.8)
    # hole Fermi level plot
    ax.plot(df_be.coords[0].value,df_be.variables[5].value, color='green',  linestyle='dotted', linewidth=1.8)
    
    ax.set_xlabel(f"{x.name} [{x.unit}]")
    ax.set_ylabel('Energy [eV]')
    ax.set_title('Energy resolved electron density at '+str(bias)+' V')
    fig.tight_layout()
    # plt.show()
    fig.savefig(file_elec+'.jpg', facecolor='white')
    
    
    #===========================
    # Energy-resolved hole density
    #===========================
    file_hole = os.path.join(folder_output,my_input_file_no_extension+r'\bias_'+i+r'\hole_density_vs_energy.fld') 
    #  file = os.path.join(folder_output,input_file_name_variable+r'\Results'+r'\LocalDOS_sg1_deg1.vtr')
    datafile_2d = nn.DataFile(file_hole,product=software)
    
    x=datafile_2d.coords['x']
    y=datafile_2d.coords['y']
    z_hole=datafile_2d.variables[0]
    
    fig, ax = plt.subplots(1)
    pcolor = ax.pcolormesh(x.value,y.value,z_hole.value.T, vmin=0.00, vmax=2.00*10**15)
    cbar = fig.colorbar(pcolor)
    cbar.set_label('Hole density [cm$^{-3}$eV$^{-1}$]')
    # conduction bandedge plot
    ax.plot(df_be.coords[0].value,df_be.variables[0].value, color='white', linestyle='-')
    # HH valence bandedge plot
    ax.plot(df_be.coords[0].value,df_be.variables[1].value, color='white', linestyle='-')
    # electron Fermi level plot
    ax.plot(df_be.coords[0].value,df_be.variables[4].value, color='red',  linestyle='dotted', linewidth=1.8)
    # hole Fermi level plot
    ax.plot(df_be.coords[0].value,df_be.variables[5].value, color='green',  linestyle='dotted', linewidth=1.8)
    
    ax.set_xlabel(f"{x.name} [{x.unit}]")
    ax.set_ylabel('Energy [eV]')
    ax.set_title('Energy resolved hole density at '+str(bias)+' V')
    fig.tight_layout()
    # plt.show()
    fig.savefig(file_hole+'.jpg', facecolor='white')
    
    
    #===========================
    # Energy-resolved electron and hole density
    #===========================
    z_elec_plus_hole = z_elec.value + z_hole.value
    
    fig, ax = plt.subplots(1)
    pcolor = ax.pcolormesh(x.value,y.value,z_elec_plus_hole.T, vmin=0.00, vmax=2.00*10**15)
    cbar = fig.colorbar(pcolor)
    cbar.set_label('Electron and hole densities [cm$^{-3}$eV$^{-1}$]')
    # conduction bandedge plot
    ax.plot(df_be.coords[0].value,df_be.variables[0].value, color='white', linestyle='-')
    # HH valence bandedge plot
    ax.plot(df_be.coords[0].value,df_be.variables[1].value, color='white', linestyle='-')
    # electron Fermi level plot
    ax.plot(df_be.coords[0].value,df_be.variables[4].value, color='red',  linestyle='dotted', linewidth=1.8)
    # hole Fermi level plot
    ax.plot(df_be.coords[0].value,df_be.variables[5].value, color='green',  linestyle='dotted', linewidth=1.8)
    
    ax.set_xlabel(f"{x.name} [{x.unit}]")
    ax.set_ylabel('Energy [eV]')
    ax.set_title('Energy resolved densities of hole and electron at '+str(bias)+' V', y=1.035)
    fig.tight_layout()
    # plt.show()
    elec_hole_img = os.path.join(folder_output,my_input_file_no_extension+r'\bias_'+i+r'\electron_hole_density_vs_energy.jpg')
    fig.savefig(elec_hole_img, dpi=300, facecolor='white')
    
    #===========================
    # Energy-resolved electron and hole densities in several biases
    #===========================
    if count in [2,4,8,10]:
        ax = fig_several.add_subplot(2,2,inner_count+1)
        
        pcolor = ax.pcolormesh(x.value,y.value,z_elec_plus_hole.T, vmin=0.00, vmax=2.00*10**15)
        #cbar = fig.colorbar(pcolor)
        #cbar.set_label('Electron and hole densities [cm$^{-3}$eV$^{-1}$]')
        # conduction bandedge plot
        ax.plot(df_be.coords[0].value,df_be.variables[0].value, color='white', linestyle='-')
        # HH valence bandedge plot
        ax.plot(df_be.coords[0].value,df_be.variables[1].value, color='white', linestyle='-')
        # electron Fermi level plot
        ax.plot(df_be.coords[0].value,df_be.variables[4].value, color='red',  linestyle='dotted', linewidth=1.8)
        # hole Fermi level plot
        ax.plot(df_be.coords[0].value,df_be.variables[5].value, color='green',  linestyle='dotted', linewidth=1.8)
        
        ax.set_xlabel(f"{x.name} [{x.unit}]", fontsize=8)
        ax.set_ylabel('Energy [eV]', fontsize=8)
        ax.tick_params(axis='x', labelsize=8)
        ax.tick_params(axis='y', labelsize=8)
        ax.set_title('Bias = '+str(bias)+' V', y=1.035, fontsize=8)
        
        inner_count += 1
    
    
    
    bias += 0.1
    count+=1

#cbar = fig_several.colorbar(pcolor)
#cbar.set_label('Electron and hole densities [cm$^{-3}$eV$^{-1}$]')
fig_several.suptitle('Energy resolved densities of electron and hole')
fig_several.tight_layout()
elec_hole_img_several = os.path.join(folder_output,my_input_file_no_extension+r'\bias_'+i+r'\electron_hole_density_vs_energy_several.jpg')
fig_several.savefig(elec_hole_img_several, dpi=300, facecolor='white')
plt.show()

print(f'=====================================')  
print(f'Done nextnanopy.')  
print(f'=====================================')  
