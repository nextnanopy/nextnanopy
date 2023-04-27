"""
Created: 2022/06/09
Updated: 2023/04/27

This Python script computes interband tunneling current through a highly-doped nitride heterojunction.
[nextnano++ tutorial]
https://www.nextnano.de/manual/nn_products/nextnanoplus/tutorials/tricks_and_hacks/1D_interband_tunneling_in_nitride_junction.html

The usage of this script is explained in
'InterbandTunneling_Duboz2019_doc.ipynb'.

For the equations and approximations, please refer to the the documentation
'InterbandTunneling_Duboz2019_formulation.pdf'.

This scripts uses the shortcut methods in Chikuwaq/nextnanopy-wrapper:
https://github.com/Chikuwaq/nextnanopy-wrapper

@author: takuma.sato@nextnano.com
"""

# Python libraries
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import simps

# nextnanopy
import nextnanopy as nn
from nextnanopy.utils.misc import mkdir_if_not_exist

# shortcuts
from nnShortcuts.common import CommonShortcuts
s = CommonShortcuts()
from nnHelpers import SweepHelper

# stopwatch
import timeit
start = timeit.default_timer()


# ===== user definition begin ===================================

#================================================================
# Specify your input file WITH EXTENSION
#================================================================
folder_path = r'D:\nextnano Users\takuma.sato\OneDrive - nextnano GmbH\Quantimony\Input files'

# input file
filename = 'InterbandTunneling_Duboz2019_nnp.in'


#================================================================
# Modify the input parameters & simulation settings
#================================================================
num_ev_CB = 30              # number of conduction band eigenvalues (without spin)
num_of_valence_bands = 6    # how many valence bands to be considered in the transition matrix. (min: 1, max: 6)

layer_thickness = 20   # thickness of p- and n-region [nm]

# bias sweep
SweepVariable = 'BIAS'
sweep_ranges =  {
    SweepVariable: ([-0.2, -1.0], 9)  # ([min, max], number of points)
}

# choose either 6-band k.p or single-band simulation for the valence band. You can also set both to False when you do not want to run simulation (only postprocessing with KP6 output data).
Run_KP6 = True   # run 6-band k.p simulation
# Run_KP6 = False
# Run_SingleBand = True   # run single-band (HH, LH, SO) simulation
Run_SingleBand = False


RemoveInputFile = True   # remove the temporary input file(s) after bias sweep
# RemoveInputFile = False   # keep the temporary input file(s) in the input folder

CalculateEffectiveField_fromOutput = True   # calculate effective field from nextnano output
# CalculateEffectiveField_fromOutput = False   # specify effective field by hand
# user_defined_effective_field = 1.0   # [V/nm] test

KaneParameter_fromOutput = True   # use nextnano database value for k.p Kane parameter
# KaneParameter_fromOutput = False   # specify Kane parameter by hand
# user_defined_Kane_EP1 = 15   # E_P1 [eV] Duboz2019

# CalculateReducedMass_fromOutput = True   # calculate reduced mass from nextnano output
CalculateReducedMass_fromOutput = False   # specify reduced mass by hand
user_defined_mass_r = 0.18 * s.electron_mass                # m_r [kg] Duboz2019

# highest valence band. Necesarry info for bandgap calculation, but does not make much difference in dipole matrix element
highestVB = 'LH'

#================================================================
# Select output figure format
#================================================================
# FigFormat = '.pdf'
# FigFormat = '.svg'
# FigFormat = '.jpg'
FigFormat = '.png'


# ===== user definition END =====================================

#%% nextnanopy pre-processing
DoNotRunSimulation = False

# decide simulation type
if Run_KP6 and Run_SingleBand:
    raise RuntimeError('nextnano can only run either multiband or single-band simulation for valence band. Do not set Run_KP6 = Run_SingleBand = True.')
if not Run_KP6 and not Run_SingleBand:
    print('KP6 and single-band simulations skipped.')
    DoNotRunSimulation = True
    simulation_type = 'kp6'
if Run_KP6 and not Run_SingleBand:
    simulation_type = 'kp6'
if not Run_KP6 and Run_SingleBand:
    simulation_type = 'SingleBand'


# number of valence band eigenvalues
if Run_KP6 or DoNotRunSimulation:
    num_ev_VB = num_of_valence_bands * num_ev_CB
elif Run_SingleBand:
    num_ev_VB = num_ev_CB

# To import Kane parameter from the nextnano database, you have to run (fast) 8-band k.p simulation.
RunKP8 = KaneParameter_fromOutput


# load the input file
InputPath  = os.path.join(folder_path, filename)
input_file = nn.InputFile(InputPath)

# automatically detect the software
software, FileExtension = s.detect_software_new(input_file)
filename_no_extension = s.separate_extension(filename)[0]

# Define output folders based on .nextnanopy-config file. If they do not exist, they are created.
folder_output = nn.config.get(software, 'outputdirectory')
folder_output_python = os.path.join(folder_output, os.path.join(r'nextnanopy', filename_no_extension))
mkdir_if_not_exist(folder_output_python)

# modify the parameters in the input file
input_file.set_variable('num_ev_CB', value=num_ev_CB)
input_file.set_variable('num_ev_VB', value=num_ev_VB)
input_file.set_variable('Thickness', value=layer_thickness)


print('Modified input parameter: ', input_file.get_variable('num_ev_CB').text)
print('Modified input parameter: ', input_file.get_variable('num_ev_VB').text)
print('Modified input parameter: ', input_file.get_variable('Thickness').text)
print('')




#%% Run nextnano simulations

# To obtain kp parameters, (fast) 8-band k.p simulation must be performed.
if RunKP8:
    print('\n------------------------------------------')
    print(f'Running {software} 8-band k.p simulation to obtain material parameters...')
    print('------------------------------------------\n')

    # adjust simulation settings in the input file
    input_file.set_variable('RunKP8',      value=1)
    input_file.set_variable('Single_band', value=0)
    input_file.set_variable('Multi_band',  value=0)

    # put bias to zero
    input_file.set_variable('BIAS', value=0.0)

    filename_kp8 = filename.replace(FileExtension, '_kp8' + FileExtension)
    InputPath_kp8 = os.path.join(folder_path, filename_kp8)
    input_file.save(InputPath_kp8, overwrite=True, automkdir=True)
    input_file.execute(convergenceCheck=True, delete_input_files=RemoveInputFile)
else:
    print('KP8 calculation skipped.')


# adjust simulation settings in the input file for 6-band or single-band simulation
input_file.set_variable('RunKP8',      value=0,                 ) # do not perform 8-band k.p in the following
input_file.set_variable('Single_band', value=int(Run_SingleBand))
input_file.set_variable('Multi_band',  value=int(Run_KP6),      )

# give a new name to the modified input file and save it
filename_temporary = filename.replace(FileExtension, '_' + simulation_type + FileExtension)
InputPath_temporary = os.path.join(folder_path, filename_temporary)
input_file.save(InputPath_temporary, overwrite=True)

# instantiate nextnanopy-wrapper.SweepHelper to facilitate simulation execution and postprocessing
helper = SweepHelper(sweep_ranges, input_file)


if Run_KP6 or Run_SingleBand:
    print('\n------------------------------------------')
    print(f'Running {software} {simulation_type} simulation')
    print('------------------------------------------\n')
    helper.execute_sweep(parallel_limit=4) # overwrite=True to avoid enumeration of output folders for secure output data access

    if RemoveInputFile:
        helper.delete_input_files()


#%% Postprocessing (calculate tunnel current)

# data containers for the I-V curve
voltages = list()
currents = list()

# Read out simulation results and calculate tunnel current for each bias
for sweep_coords, sweep_subfolder in zip(helper.data['sweep_coords'], helper.data['output_subfolder']):

    SweepValue = sweep_coords[0]  # one-dimensional sweep

    print('\n------------------------------------------')
    print(f"nextnanopy postprocessing for {SweepVariable}={SweepValue}")
    print('------------------------------------------\n')

    # extract values from simulation - electrostatic potential gradient
    df_potential = helper.shortcuts.get_DataFile_in_folder('potential.dat', sweep_subfolder)
    x = df_potential.coords['x'].value      # this is the simulation grid

    if CalculateEffectiveField_fromOutput:

        Potential = df_potential.variables['Potential'].value
        PotentialGrad = np.gradient(Potential, x)   # derivative

        fig, ax1 = plt.subplots()
        color = 'tab:red'
        ax1.plot(x, Potential, color=color)
        ax1.set_xlabel(f'{df_potential.coords["x"].label}')
        ax1.set_ylabel(f'{df_potential.variables["Potential"].label}', color=color)
        # ax1.set_title('Electrostatic potential and its gradient')
        ax1.tick_params(axis='y', labelcolor=color)

        ax2 = ax1.twinx()   # instantiate a second axes that shares the same x-axis
        color = 'tab:blue'
        ax2.set_ylabel('Gradient (V/nm)', color=color)
        ax2.plot(x, PotentialGrad, color=color, label=f'{SweepVariable}={SweepValue}')
        ax2.tick_params(axis='y', labelcolor=color)
        ax2.legend()
        fig.tight_layout()
        plt.show()
        print('PLOT: electrostatic potential and its gradient')

    elif not user_defined_effective_field:
        raise RuntimeError('Please specify effective field [V/nm] or set CalculateEffectiveField_fromOutput = True.')
    else:
        PotentialGrad = np.array([user_defined_effective_field] * len(x))   # user-defined effective field
        print('Using user-defined effective field...')


    # extract values from simulation - conduction band envelope functions
    print('Reading in the envelope functions...')
    print('No. of conduction band eigenvalues (without spin degeneracy) = ', num_ev_CB)
    print('No. of valence band eigenvalues (considering different spin states) = ', num_ev_VB)

    df_amplitudeGamma = helper.shortcuts.get_DataFile_in_folder(['amplitudes_QuantumRegion', 'Gamma'], sweep_subfolder)
    # x = df_amplitudeGamma.coords['x'].value  # numpy.array
    amplitude_Gamma = np.zeros((num_ev_CB, len(x)), dtype = np.float64)    # (CB eigenvalue index, position x). For effective mass model the amplitude is a real function.
    for i in range(num_ev_CB):
        amplitude_Gamma[i,] = df_amplitudeGamma.variables[f'Psi_{i+1}'].value   # envelope amplitude


    # extract values from simulation - valence band complex envelope functions
    if Run_KP6 or DoNotRunSimulation:
        df_amplitudeVB = helper.shortcuts.get_DataFile_in_folder(['amplitudes_QuantumRegion', 'SXYZ'], sweep_subfolder)
        amplitude_VB_x1 = np.zeros((num_ev_VB, len(x)), dtype = np.complex128)          # (VB eigenvalue index, position x). For k.p model the amplitude is a complex function.
        amplitude_VB_x2 = np.zeros((num_ev_VB, len(x)), dtype = np.complex128)          # In nn++, x, y, and z components refers to the simulation coordinates and not the crystal coordinates. Growth direction = x.
        for j in range(num_ev_VB):
            for pos in range(len(x)):
                amplitude_VB_x1[j, pos] = complex(df_amplitudeVB.variables[f'Psi_{j+1}_x1_real'].value[pos], df_amplitudeVB.variables[f'Psi_{j+1}_x1_imag'].value[pos])   # envelope amplitude
                amplitude_VB_x2[j, pos] = complex(df_amplitudeVB.variables[f'Psi_{j+1}_x2_real'].value[pos], df_amplitudeVB.variables[f'Psi_{j+1}_x2_imag'].value[pos])
    elif Run_SingleBand:
        df_amplitudeVB = helper.shortcuts.get_DataFile_in_folder('amplitudes_QuantumRegion_SO', sweep_subfolder)
        amplitude_VB_SO = np.zeros((num_ev_VB, len(x)), dtype = np.float64)
        for j in range(num_ev_VB):
            for pos in range(len(x)):
                amplitude_VB_SO[j,] = df_amplitudeVB.variables[f'Psi_{j+1}'].value   # envelope amplitude




    # extract values from simulation - bandgap
    print('Extracting bandgap...')
    df_bandgap = helper.shortcuts.get_DataFile_in_folder('bandgap.dat', sweep_subfolder)
    bandgap_gamma = s.scale_eV_to_J * df_bandgap.variables['Bandgap_Gamma'].value



    # extract values from simulation - crystal-field and spin-orbit splitting
    print('Reading in the position-dependent material parameters...')
    df_splitting = helper.shortcuts.get_DataFile('spin_orbit_coupling_energies.dat', filename_kp8)
    Crystal_splitting = s.scale_eV_to_J * df_splitting.variables['Delta_1'].value     # Delta_1 = Delta_crystal
    SpinOrbit_splitting = s.scale_eV_to_J * df_splitting.variables['Delta_2'].value   # Delta_2 = Delta_parallel

    # convert from material grid to simulation grid
    x_material_grid = df_splitting.coords['x'].value   # material grid
    Crystal_splitting_on_sim_grid   = s.convert_grid(Crystal_splitting, x_material_grid, x)
    SpinOrbit_splitting_on_sim_grid = s.convert_grid(SpinOrbit_splitting, x_material_grid, x)

    # obtain Kane parameter P_1
    if KaneParameter_fromOutput:
        # extract values from simulation - Kane parameter
        df_kpParam = helper.shortcuts.get_DataFile(['kp_parameters', 'kp8'], filename_kp8)
        Kane_P1 = s.scale_eV_to_J * s.scale_Angstrom_to_nm * df_kpParam.variables['P1'].value   # P_1 = along the c crystal axis. Units translated to [J nm]
        Kane_P1_on_sim_grid = s.convert_grid(Kane_P1, x_material_grid, x)   # convert from material to simulation grid
    elif not user_defined_Kane_EP1:
        raise RuntimeError('Please specify Kane energy parameter [eV] or set KaneParameter_fromOutput = True.')
    else:
        P1 = s.scale1ToNano * np.sqrt(s.hbar**2 * (s.scale_eV_to_J * user_defined_Kane_EP1) / 2 / s.electron_mass)   # user-defined Kane parameter. Units translated to [J nm]
        Kane_P1_on_sim_grid = np.array([P1] * len(x))



    # bandedge shift due to crystal splitting and spin-orbit coupling
    SpinOrbit_splitting_perp_on_sim_grid = SpinOrbit_splitting_on_sim_grid   # nextnano database assumes delta_perp = delta_para
    bandshift_HH = Crystal_splitting_on_sim_grid + SpinOrbit_splitting_on_sim_grid
    p = (Crystal_splitting_on_sim_grid - SpinOrbit_splitting_on_sim_grid) / 2.
    bandshift_LH = p + np.sqrt(p**2 + 2*SpinOrbit_splitting_perp_on_sim_grid**2)


    # calculate dipole_moment = <Z|z|S> = P1/Eg
    if highestVB == 'HH':
        Eg = bandgap_gamma + bandshift_HH
    elif highestVB == 'LH':
        Eg = bandgap_gamma + bandshift_LH
    else:
        raise RuntimeError('Please specify the highest valence band (HH or LH).')

    dipole_moment = Kane_P1_on_sim_grid / Eg


    # for single band, coefficient beta' is needed
    beta_squared = bandshift_LH**2 / (bandshift_LH**2 + 2*SpinOrbit_splitting_on_sim_grid**2)


    # remove the grid points within contacts, and
    # cut off the edges by one more grid to exclude the effect of contact on dipole moment.
    # (Contacts should be excluded from the integration because the bandgap is zero.)
    indices_in_contacts = [ i for i in range(len(x)) if bandgap_gamma[i] == 0 ]

    dipole_moment_cut = np.delete(dipole_moment, indices_in_contacts)
    PotentialGrad_cut = np.delete(PotentialGrad, indices_in_contacts)
    x_cut             = np.delete(x, indices_in_contacts)
    beta_squared_cut  = np.delete(beta_squared, indices_in_contacts)   # for single band
    print(f'Integration performed from x = {x_cut[0]} to {x_cut[-1]}')

    amplitude_Gamma_cut = np.zeros((num_ev_CB, len(x_cut)), dtype=np.float64)
    for i in range(num_ev_CB):
            amplitude_Gamma_cut[i,] = np.delete(amplitude_Gamma[i,], indices_in_contacts)

    if Run_KP6 or DoNotRunSimulation:
        amplitude_VB_x1_cut = np.zeros((num_ev_VB, len(x_cut)), dtype=np.complex128)
        amplitude_VB_x2_cut = np.zeros((num_ev_VB, len(x_cut)), dtype=np.complex128)
        for j in range(num_ev_VB):
            amplitude_VB_x1_cut[j,] = np.delete(amplitude_VB_x1[j,], indices_in_contacts)
            amplitude_VB_x2_cut[j,] = np.delete(amplitude_VB_x2[j,], indices_in_contacts)
    elif Run_SingleBand:
        amplitude_VB_SO_cut = np.zeros((num_ev_VB, len(x_cut)), dtype=np.complex128)
        for j in range(num_ev_VB):
            amplitude_VB_SO_cut[j,] = np.delete(amplitude_VB_SO[j,], indices_in_contacts)





    if Run_KP6 or DoNotRunSimulation:
        # calculate the integrand for each spin
        integrand1 = np.zeros((num_ev_CB, num_ev_VB, len(x_cut)), dtype = np.complex128)  # create a (num_ev_CB * num_ev_VB) matrix with position-dependent elements
        integrand2 = np.zeros((num_ev_CB, num_ev_VB, len(x_cut)), dtype = np.complex128)
        for i in range(num_ev_CB):
            for j in range(num_ev_VB):
                integrand1[i, j, ] = dipole_moment_cut * np.conjugate(amplitude_VB_x1_cut[j, ]) * amplitude_Gamma_cut[i, ] * s.elementary_charge * PotentialGrad_cut
                integrand2[i, j, ] = dipole_moment_cut * np.conjugate(amplitude_VB_x2_cut[j, ]) * amplitude_Gamma_cut[i, ] * s.elementary_charge * PotentialGrad_cut

        # integrate over position
        integral1 = simps(integrand1, x_cut)   # [J/nm] integrated over [nm] gives [J]
        integral2 = simps(integrand2, x_cut)
        print('Transition matrix (row, column): ', np.shape(integral1))

        # read in the spinor composition from nextnano output
        df_spinor = helper.shortcuts.get_DataFile_in_folder(['spinor_composition', 'SXYZ'], sweep_subfolder)
        spinor_x1_squared = df_spinor.variables['x1'].value   # list of spinor x1 components squared for all eigenstates j
        spinor_x2_squared = df_spinor.variables['x2'].value   # list of spinor x2 components squared for all eigenstates j

        # multiply by spinor components & sum over spin
        M_absoluteSquared_spinsum = np.zeros((num_ev_CB, num_ev_VB), dtype = np.float64)
        for i in range(num_ev_CB):
            for j in range(num_ev_VB):
                M_absoluteSquared_spinsum[i,j] = spinor_x1_squared[j] * np.absolute(integral1[i,j]) **2
                M_absoluteSquared_spinsum[i,j] += spinor_x2_squared[j] * np.absolute(integral2[i,j]) **2

    elif Run_SingleBand:
        # calculate the integrand
        integrand = np.zeros((num_ev_CB, num_ev_VB, len(x_cut)), dtype = np.complex128)  # create a (num_ev_CB * num_ev_VB) matrix with position-dependent elements
        for i in range(num_ev_CB):
            for j in range(num_ev_VB):
                integrand[i, j, ] = np.sqrt(beta_squared_cut) * dipole_moment_cut * amplitude_VB_SO_cut[j, ] * amplitude_Gamma_cut[i, ] * s.elementary_charge * PotentialGrad_cut

        # integrate over position
        M = simps(integrand, x_cut)   # [J/nm] integrated over [nm] gives [J]


        # sum over spin
        M_absoluteSquared_spinsum = 2 * np.absolute(M) * np.absolute(M)





    # reduced mass
    if CalculateReducedMass_fromOutput:
        # extract values from simulation - mass
        print('Extracting masses and calculating reduced mass...')
        df_mass = helper.shortcuts.get_DataFile_in_folder('charge_carrier_masses.dat', sweep_subfolder)
        mass_CB = df_mass.variables['Gamma_mass_t'].value       # effective mass along in-plane direction [unit: m_0]
        mass_VB = df_mass.variables['SO_mass_t'].value          # we take SO effective mass as it contributes dominantly.

        # translate to the simulation grid
        mass_CB_on_sim_grid = s.convert_grid(mass_CB, x_material_grid, x)
        mass_VB_on_sim_grid = s.convert_grid(mass_VB, x_material_grid, x)

        # calculate reduced mass m_r
        mass_r = s.electron_mass * mass_CB_on_sim_grid * mass_VB_on_sim_grid / (mass_CB_on_sim_grid + mass_VB_on_sim_grid)
        mass_r_averaged = np.average(mass_r)   # average the reduced mass over the system ???

    elif not user_defined_mass_r:   # if the variable is empty
        raise RuntimeError('Please specify the reduced mass, or set CalculateReducedMass_fromOutput = True.')
    else:
        mass_r_averaged = user_defined_mass_r
        print('Using user-defined reduced mass...')





    # calculate tunnel current for the transition j -> i
    I_ij = s.scale1ToCenti**(-2) * s.elementary_charge * mass_r_averaged * M_absoluteSquared_spinsum / s.hbar**3   # [A/cm^2]


    # sum over possible transitions (energy levels)
    I = 0.
    num_possible_transitions = 0
    df_ev_CB     = helper.shortcuts.get_DataFile_in_folder(['energy_spectrum', 'Gamma'], sweep_subfolder)

    if Run_KP6 or DoNotRunSimulation:
        df_ev_VB = helper.shortcuts.get_DataFile_in_folder(['energy_spectrum', 'kp6'], sweep_subfolder)
    elif Run_SingleBand:
        df_ev_VB = helper.shortcuts.get_DataFile_in_folder(['energy_spectrum', 'SO'], sweep_subfolder)


    for i in range(num_ev_CB):
        eigenvalue_CB = df_ev_CB.variables['Energy'].value[i]

        for j in range(num_ev_VB):
            eigenvalue_VB = df_ev_VB.variables['Energy'].value[j]
            if eigenvalue_VB >= eigenvalue_CB:
                I += I_ij[i][j]
                num_possible_transitions += 1
                print(f'possible transition VB{j+1} --> CB{i+1}')
    print(f'\nNumber of possible transitions at the bias {SweepValue}: {num_possible_transitions} out of ', num_ev_CB * num_ev_VB)

    voltages.append(-SweepValue)   # minus sign converts the backward bias to positive values
    currents.append(I)


    # wave function overlap. Not used during simulation, for reference
    sum_overlap_squared = 0.
    for i in range(num_ev_CB):
        eigenvalue_CB = df_ev_CB.variables['Energy'].value[i]
        for j in range(num_ev_VB):
            eigenvalue_VB = df_ev_VB.variables['Energy'].value[j]
            if Run_KP6 or DoNotRunSimulation:
                overlap = simps(np.conjugate(amplitude_VB_x1_cut[j,]) * amplitude_Gamma_cut[i,], x_cut)
            elif Run_SingleBand:
                overlap = simps(amplitude_VB_SO_cut[j,] * amplitude_Gamma_cut[i,], x_cut)

            if eigenvalue_VB >= eigenvalue_CB:
                sum_overlap_squared += np.absolute(overlap)**2
    print('\nij-sum of envelope overlap squared (not used during simulation, for reference): ', sum_overlap_squared)



# plot m_r in units of s.electron_mass
if CalculateReducedMass_fromOutput:
    fig, ax = plt.subplots()
    ax.plot(x, mass_r / s.electron_mass)
    ax.set_xlabel(f"{df_potential.coords['x'].label}")
    ax.set_ylabel('(m_0)')
    ax.set_title('Reduced mass')
    print('\nPLOT: reduced mass\n')

# plot material parameters & dipole moment (independent of bias)
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
ax1.plot(x, bandgap_gamma / s.scale_eV_to_J , label='bandgap c-hh [eV]')
ax1.plot(x, Crystal_splitting_on_sim_grid / s.scale_eV_to_J, label='crystal splitting [eV]')
ax1.plot(x, SpinOrbit_splitting_on_sim_grid / s.scale_eV_to_J, label='spin-orbit splitting [eV]')
if KaneParameter_fromOutput:
    ax1.plot(x, Kane_P1_on_sim_grid / s.scale_eV_to_J, label='Kane parameter P1 [eV nm]')
ax1.set_xlabel(f"{df_potential.coords['x'].label}")
ax1.set_title('Position-dependent material parameters')
ax1.legend(bbox_to_anchor=(1,1), loc='upper left')

ax2.plot(x_cut, dipole_moment_cut)
ax2.set_xlabel(f"{df_potential.coords['x'].label}")
ax2.set_ylabel('(nm)')
ax2.set_title('dipole matrix element <Z|z|S>')
fig.tight_layout()
print('\nPLOT: bandgap, position-dependent material parameters and dipole moment\n')


# tunnel current vs. bias plot
fig, ax = plt.subplots()
plt.yscale('log')
plt.ylim([1e-6, 1e1])
ax.plot(voltages, currents, 'o-')
ax.set_xlabel('bias [V]')
ax.set_ylabel('[A/cm^2]')
ax.set_title('Tunnel current simulated by 6-band k.p model')
fig.savefig(os.path.join(folder_output_python,'TunnelCurrent_vs_bias' + FigFormat))  # save plot

# tunnel current vs. bias data file
a = os.path.join(folder_output_python, f'TunnelCurrent_vs_bias_{simulation_type}.dat')
with open(a, 'w') as f:
    f.write('bias(V)\ttunnel current(A/cm^2)\n')
    for bias, current in zip(voltages, currents):
        f.write(f'{bias}\t{current}')
        f.write('\n')
print(f'\nTotal tunnel current has been plotted and saved in the folder {folder_output_python}\n')


stop = timeit.default_timer()
runtime_sec = stop - start
runtime_min = runtime_sec / 60
print('-------------------------------------------------------------')
print('nextnanopy DONE.')
print(f'Run Time ({software} and nextnanopy): {runtime_sec:.3f} [sec]  ({runtime_min:.3f} [min])' )
print('-------------------------------------------------------------')
