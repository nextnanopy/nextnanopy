# -*- coding: utf-8 -*-
"""
Created: 2021/05/27
Updated: 2022/06/10

Basic toolbox (shortcut, module) for nextnanopy. Basis of nnp_shortcuts and NEGF_shortcuts.

@author: takuma.sato@nextnano.com
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf as backendPDF
import nextnanopy as nn
from nextnanopy.utils.misc import mkdir_if_not_exist
# from PIL import Image   # for gif
# from celluloid import Camera   # for gif
# from IPython.display import HTML   # for HTML display of gif

# fundamental physical constants https://physics.nist.gov/cgi-bin/cuu
hbar = 1.054571817E-34   # Planck constant / 2Pi in [J.s]
electron_mass = 9.1093837015E-31   # in [kg]
elementary_charge  = 1.602176634*10**(-19)   # [C] elementary charge

scale1ToKilo = 1e-3
scale1ToCenti = 1e2
scale1ToMilli = 1e3
scale1ToMicro = 1e6
scale1ToNano = 1e9

scale_Angstrom_to_nm = 0.1
scale_eV_to_J = elementary_charge


class NextnanopyScriptError(Exception):
    """ Exception when the user's Python script contains issue """
    pass

class NextnanoInputFileError(Exception):
    """ Exception when the user's nextnano input file contains issue """
    pass


# -------------------------------------------------------
# Simulation preprocessing
# -------------------------------------------------------

def separateFileExtension(filename):
    """
    Separate file extension from file name.
    Returns the original filename and empty string if extension is absent.
    """
    filename = os.path.split(filename)[1]   # remove paths if present

    if filename[-3:] == '.in':
        extension = '.in'
    elif filename[-4:] == '.xml':
        extension = '.xml'
    elif filename[-5:] == '.negf':
        extension = '.negf'
    else:
        extension = ''

    filename_no_extension = filename.replace(extension, '')
    return filename_no_extension, extension



def detect_software(folder_path, filename):
    """
    Detect software from input file for the argument of nextnanopy.DataFile() and sweep output folder names.
    The return value software will be needed for the argument of nextnanopy.DataFile() and sweep output folder names.

    Parameters
    ----------
    folder_path : str
        input file folder
    filename : str
        input file name

    Returns
    -------
    software : str
        nextnano solver
    software_short : str
        shorthand of nextnano solver
    extension : str
        file extension
    """

    extension = separateFileExtension(filename)[1]
    if extension == '':
        raise ValueError('Please specify input file with extension (.in, .xml or .negf)')

    InputPath = os.path.join(folder_path, filename)
    try:
        with open(InputPath,'r') as file:
            for line in file:
                if 'simulation-flow-control' in line:
                    software = 'nextnano3'
                    software_short = '_nn3'
                    break
                elif 'run{' in line:
                    software = 'nextnano++'
                    software_short = '_nnp'
                    break
                elif '<nextnano.NEGF' in line or 'nextnano.NEGF{' in line:
                    software = 'nextnano.NEGF'
                    software_short = '_nnNEGF'
                    break
                elif '<nextnano.MSB' in line or 'nextnano.MSB{' in line:
                    software = 'nextnano.MSB'
                    software_short = '_nnMSB'
    except FileNotFoundError:
        raise FileNotFoundError(f'Input file {InputPath} not found!')

    if not software:   # if the variable is empty
        raise NextnanoInputFileError('Software cannot be detected! Please check your input file.')
    else:
        print('\nSoftware detected: ', software)

    return software, software_short, extension



def detect_software_new(inputfile):
    """
    Detect software from nextnanopy.InputFile() object.
    The return value software will be needed for the argument of nextnanopy.DataFile() and sweep output folder names.

    This function is more compact than detect_software() because it makes use of the attributes of nextnanopy.InputFile() object.
    If the object is not executed in the script, it does not have execute_info attributes.
    In that case, you have to explicitly give the output folder name to load output data.
    Therefore, THIS METHOD DOES NOT WORK IF YOU RUN SIMULATIONS WITH nextnanopy.Sweep()!
    """
    try:
        with open(inputfile.fullpath, 'r') as file:
            for line in file:
                if 'simulation-flow-control' in line:
                    software = 'nextnano3'
                    extension = '.in'
                    break
                elif 'run{' in line:
                    software = 'nextnano++'
                    extension = '.in'
                    break
                elif '<nextnano.NEGF' in line:
                    software = 'nextnano.NEGF'
                    extension = '.xml'
                    break
                elif 'nextnano.NEGF{' in line:
                    software = 'nextnano.NEGF'
                    extension = '.negf'
                elif '<nextnano.MSB' in line:
                    software = 'nextnano.MSB'
                    extension = '.xml'
                elif 'nextnano.MSB{' in line:
                    software = 'nextnano.MSB'
                    extension = '.negf'
    except FileNotFoundError:
        raise FileNotFoundError(f'Input file {inputfile.fullpath} not found!')

    if not software:   # if the variable is empty
        raise NextnanoInputFileError('Software cannot be detected! Please check your input file.')
    else:
        print('\nSoftware detected: ', software)

    return software, extension



def prepareInputFile(folderPath, originalFilename, modifiedParamString='', newValue=0, filename_appendix=''):
    """
    Modify parameter in the input file, append specified string to the file name, save the file.

    RETURN:
        new file name
        modified nextnanopy.InputFile object
    """
    InputPath     = os.path.join(folderPath, originalFilename)
    input_file    = nn.InputFile(InputPath)

    if modifiedParamString == '':
        print('\nUsing the default parameters in the input file...\n')
        return originalFilename, input_file

    input_file.set_variable(modifiedParamString, value=newValue)
    name = input_file.get_variable(modifiedParamString).name
    value = input_file.get_variable(modifiedParamString).value
    print(f'\nUsing modified input parameter:\t${name} = {value}')

    filename_no_extension, extension = separateFileExtension(originalFilename)
    if extension == '':
        raise ValueError('Include file extension to the input file name!')
    newFilename = filename_no_extension + filename_appendix + extension
    print(f'Saving input file as:\t{newFilename}\n')
    input_file.save(os.path.join(folderPath, newFilename), overwrite=True)   # update input file name

    return newFilename, input_file


def mass_from_kp_parameters(db_Ep, db_S, eff_mass, Eg, deltaSO):
    factor = (Eg + 2. * deltaSO / 3.) / Eg / (Eg + deltaSO)   # independent of S and Ep, but temperature-dependent
    mass = 1. / (db_S + db_Ep * factor)
    return mass


# TODO: extend to WZ
def evaluate_and_rescale_S(db_Ep, db_S, db_L, db_N, eff_mass, Eg, deltaSO, evaluateS, rescaleS, rescaleSTo):
    """
    Identical to nnp implementation. 'db_' denotes database values.
    massFromKpParameters changes mass, but it isn't used to rescale S here because
    (*) old_S + old_Ep * factor = new_S + new_Ep * factor
    NEGF uses mass when rescaling S.
    """
    factor = (Eg + 2. * deltaSO / 3.) / Eg / (Eg + deltaSO)   # independent of S and Ep, but temperature-dependent

    if evaluateS:
        S = 1. / eff_mass - db_Ep * factor
    else:
        S = db_S


    if rescaleS:   # rescale S to given value, and adjust Ep to preserve the effective mass
        new_S = rescaleSTo
        new_Ep = db_Ep + (S - new_S) / factor   # using formula (*)
    else:
        new_Ep = db_Ep
        new_S = S

    if (isinstance(new_Ep, float) and new_Ep < 0) or (hasattr(new_Ep, '__iter__') and any(x < 0 for x in new_Ep)):
        raise RuntimeError('Ep parameter has become negative while rescaling S!')

    # L' and N' get modified by the change of Ep
    cSchroedinger = hbar**2 / 2 / electron_mass
    new_L = db_L + cSchroedinger * (new_Ep - db_Ep) / Eg
    new_N = db_N + cSchroedinger * (new_Ep - db_Ep) / Eg

    return new_S, new_Ep, new_L, new_N



# TODO: extend to WZ
def rescale_Ep_and_get_S(old_Ep, old_S, old_L, old_N, rescaleEpTo, Eg, deltaSO):
    """
    Rescale Ep to given value, and adjust S to preserve the electron effective mass:
    (*) old_S + old_Ep * factor = new_S + rescaleEpTo * factor
    """
    factor = (Eg + 2.*deltaSO/3.) / Eg / (Eg + deltaSO)   # independent of S and Ep, but temperature-dependent
    new_S = old_S + (old_Ep - rescaleEpTo) * factor

    # L' and N' get modified by the change of Ep
    cSchroedinger = hbar**2 / 2 / electron_mass
    new_L = old_L + cSchroedinger * (rescaleEpTo - old_Ep) / Eg
    new_N = old_N + cSchroedinger * (rescaleEpTo - old_Ep) / Eg
    return new_S, new_L, new_N



# -------------------------------------------------------
# Access to output data
# -------------------------------------------------------

def check_if_simulation_has_run(input_file):
    """
    Check if simulation has been run. If not, ask the user if the postprocessing should continue.

    INPUT:
        input_file      nn.InputFile() object
    """
    try:
        folder = input_file.folder_output
    except:
        determined = False
        while not determined:
            choice = input('Simulation has not been executed. Continue? [y/n]')
            if choice == 'n':
                raise RuntimeError('Nextnanopy terminated.')
            elif choice == 'y':
                determined = True
            else:
                print("Invalid input.")
                continue


def getSweepOutputFolderName(filename, *args):
    """
    nextnanopy.sweep.execute_sweep() generates output folder with this name

    INPUT:
        filename
        args = SweepVariableString1, SweepVariableString2, ...

    RETURN:
        string of sweep output folder name

    """
    filename_no_extension = separateFileExtension(filename)[0]
    output_folderName = filename_no_extension + '_sweep'

    for sweepVar in args:
        if not isinstance(sweepVar, str):
            raise TypeError(f'Argument {sweepVar} must be a string!')
        output_folderName += '__' + sweepVar

    return output_folderName


def getSweepOutputFolderPath(filename, software, *args):
    """
    Get the output folder path generated by nextnanopy.sweep.execute_sweep().

    Parameters
    ----------
    filename : str
        input file name (may include absolute/relative paths)
    software : str
        nextnano solver
    *args : str
        SweepVariableString1, SweepVariableString2, ...

    Raises
    ------
    base.NextnanopyScriptError
        If any of the arguments are invalid.

    Returns
    -------
    output_folder_path : str
        sweep output folder path

    """
    filename_no_extension = separateFileExtension(filename)[0]
    output_folder_path = os.path.join(nn.config.get(software, 'outputdirectory'), filename_no_extension + '_sweep')

    if len(args) == 0: raise ValueError("Sweep variable string is missing in the argument!")

    for sweepVar in args:
        if not isinstance(sweepVar, str):
            raise TypeError(f'Argument {sweepVar} must be a string!')
        output_folder_path += '__' + sweepVar

    return output_folder_path


def get_output_subfolder_path(sweep_output_folder_path, input_file_name):
    """
    Return output folder path corresponding to the input file

    Parameters
    ----------
    input_file_name : str
        input file name or path

    Returns
    -------
    str
        path to output folder

    """
    subfolder_name = separateFileExtension(input_file_name)[0]
    return os.path.join(sweep_output_folder_path, subfolder_name)


def getSweepOutputSubfolderName(filename, sweepCoordinates):
    """
    nextnanopy.sweep.execute_sweep() generates output subfolders with this name

    INPUT:
        filename
        {sweepVariable1: value1, sweepVariable2: value2, ...}

    RETURN:
        string of sweep output subfolder name

    """
    filename_no_extension = separateFileExtension(filename)[0]
    output_subfolderName = filename_no_extension + '__'

    for sweepVar, value in sweepCoordinates.items():
        if not isinstance(sweepVar, str):
            raise TypeError('key must be a string!')
        try:
            val = str(value)
        except ValueError:
            print('value cannot be converted to string!')
            raise
        else:
            output_subfolderName +=  sweepVar + '_' + val + '_'

    return output_subfolderName



def getDataFile(keywords, name, software):
    """
    Get single nextnanopy.DataFile of output data in the directory matching name with the given string keyword.

    Parameters
    ----------
    keywords : str or list of str
        Find output data file with the names containing single keyword or multiple keywords (AND search)
    name : str
        input file name (= output subfolder name). May contain extensions and/or fullpath.
    software : str
        nextnano solver.

    Returns
    -------
    nextnanopy.DataFile object of the simulation data

    """
    outputFolder = nn.config.get(software, 'outputdirectory')
    filename_no_extension = separateFileExtension(name)[0]
    outputSubfolder = os.path.join(outputFolder, filename_no_extension)

    return getDataFile_in_folder(keywords, outputSubfolder, software)


def getDataFile_in_folder(keywords, folder_path, software):
    """
    Get single nextnanopy.DataFile of output data with the given string keyword(s) in the specified folder.

    Parameters
    ----------
    keywords : str or list of str
        Find output data file with the names containing single keyword or multiple keywords (AND search)
    folder_path : str
        absolute path of output folder in which the datafile should be sought
    software : str
        nextnano solver.

    Returns
    -------
    nextnanopy.DataFile object of the simulation data

    """
    print(f'\nSearching for output data with keyword(s) {keywords}...')

    # Search output data using nn.DataFolder.find(). If multiple keywords are provided, find the intersection of files found with each keyword.
    if isinstance(keywords, str):
        list_of_files = nn.DataFolder(folder_path).find(keywords, deep=True)
    elif isinstance(keywords, list):
        list_of_sets = [set(nn.DataFolder(folder_path).find(keyword, deep=True)) for keyword in keywords]
        candidates = list_of_sets[0]
        for s in list_of_sets:
            candidates = s.intersection(candidates)
        list_of_files = list(candidates)
    else:
        raise TypeError("Argument 'keywords' must be either str or list")

    # validate the search result
    if len(list_of_files) == 0:
        raise FileNotFoundError(f"No output file found with keyword(s) '{keywords}'!")
    elif len(list_of_files) == 1:
        file = list_of_files[0]
    else:
        print(f"More than one output files found with keyword(s) '{keywords}'!")
        for count, file in enumerate(list_of_files):
            filename = os.path.split(file)[1]
            print(f"Choice {count}: {filename}")
        determined = False
        while not determined:
            choice = input('Enter the index of data you need: ')
            if choice == 'q':
                raise RuntimeError('Nextnanopy terminated.')
            try:
                choice = int(choice)
            except ValueError:
                print("Invalid input. (Type 'q' to quit)")
                continue
            else:
                if choice < 0 or choice >= len(list_of_files):
                    print("Index out of bounds. Type 'q' to quit")
                    continue
                else:
                    determined = True
        file = list_of_files[choice]

    if __debug__: print("Found:\n", file)

    try:
        return nn.DataFile(file, product=software)
    except NotImplementedError:
        raise NotImplementedError(f'Nextnanopy does not support datafile for {file}')


def getDataFiles(keywords, name, software):
    """
    Get multiple nextnanopy.DataFiles of output data with the given string keyword(s).

    Parameters
    ----------
    keywords : str or list of str
        Find output data file with the names containing single keyword or multiple keywords (AND search).
    name : str
        input file name (= output subfolder name) without folder paths. May contain extension '.in' or '.xml'.
    software : str
        nextnano solver.

    Returns
    -------
    datafiles : list
        list of nextnanopy.DataFile objects.

    """

    outputFolder = nn.config.get(software, 'outputdirectory')
    filename_no_extension = separateFileExtension(name)[0]
    outputSubFolder = os.path.join(outputFolder, filename_no_extension)

    return getDataFiles_in_folder(keywords, outputSubFolder, software)


def getDataFiles_in_folder(keywords, folder_path, software):
    """
    Get multiple nextnanopy.DataFiles of output data with the given string keyword(s) in the specified folder.

    Parameters
    ----------
    keywords : str or list of str
        Find output data file with the names containing single keyword or multiple keywords (AND search)
    folder_path : str
        absolute path of output folder in which the datafile should be sought
    software : str
        nextnano solver.

    Returns
    -------
    nextnanopy.DataFile object of the simulation data

    """
    print(f'\nSearching for output data with keyword(s) {keywords}...')

    # Search output data using nn.DataFolder.find(). If multiple keywords are provided, find the intersection of files found with each keyword.
    if isinstance(keywords, str):
        outputFiles = nn.DataFolder(folder_path).find(keywords, deep=True)
    elif isinstance(keywords, list):
        list_of_sets = [set(nn.DataFolder(folder_path).find(keyword, deep=True)) for keyword in keywords]
        candidates = list_of_sets[0]
        for s in list_of_sets:
            candidates = s.intersection(candidates)
        outputFiles = list(candidates)
    else:
        raise TypeError("Argument 'keywords' must be either str or list")

    # validate the search result
    if len(outputFiles) == 0:
        raise FileNotFoundError(f"No output file found with keyword(s) '{keywords}'!")
    elif len(outputFiles) == 1:
        print(f"WARNING: Only one output file found with keyword(s) '{keywords}'!")

    if __debug__: print("Found:\n", outputFiles)

    try:
        datafiles = [nn.DataFile(file, product=software) for file in outputFiles]
    except NotImplementedError:
        raise NotImplementedError('Nextnanopy does not support datafile')

    return datafiles




# -------------------------------------------------------
# Data postprocessing
# -------------------------------------------------------

def convert_grid(arr, old_grid, new_grid):
    """
    Convert grid of an array.
    Needed if two physical quantities that you want to overlay are on a different grid.

    Parameters
    ----------
    arr : array-like
        array to be converted
    old_grid : array-like
        grid points on which arr is defined
    new_grid : array-like
        grid points on which new arr should sit

    Returns
    -------
    arr_new : array-like
        array on the new grid

    Requires
    --------
    SciPy
    """

    from scipy.interpolate import splev, splrep

    spl = splrep(old_grid, arr)     # interpolate
    arr_new = splev(new_grid, spl)  # map to new grid
    return arr_new



def cutOff_edges1D(arr, x_grid, start_position, end_position):
    """
    Cut off the edges of 1D real space array.

    Parameters
    ----------
    arr : array-like
        1D array to be processed
    x_grid : array-like
        grid points on which arr is defined
    start_position : float
        new array starts from this position
    end_position : float
        new array ends at this position

    Returns
    -------
    array-like
        arr without edges

    """
    if np.ndim(arr) != 1: raise ValueError("Array must be one-dimensional!")

    num_gridPoints = len(x_grid)

    # input validation
    if len(arr) != num_gridPoints:  # 'averaged = yes' 'boxed = yes' may lead to inconsistent number of grid points
        print(len(arr), num_gridPoints)
        raise ValueError('Array size does not match real space grid points')
    if start_position < x_grid[0]:
        raise ValueError('start_position out of range!')
    if end_position > x_grid[-1]:
        raise ValueError('end_position out of range!')

    # find start & end index
    for i in range(num_gridPoints-1):
        if x_grid[i] <= start_position < x_grid[i + 1]:
            start_index = i
        if x_grid[i] < end_position <= x_grid[i + 1]:
            end_index = i + 1

    return arr[start_index : end_index + 1]



def findCell(position_arr, wantedPosition):
    """
    Find the grid cell that contains given wanted position and return index.
    """
    num_gridPoints = len(position_arr)
    cnt = 0
    for i in range(num_gridPoints-1):
        if position_arr[i] <= wantedPosition < position_arr[i + 1]:
            start_index = i
            end_index = i + 1
            cnt = cnt + 1

    if cnt == 0:
        raise RuntimeError('No grid cells found that contain the point x = {wantedPosition}')
    if cnt > 1:
        raise RuntimeError(f'Multiple grid cells found that contain the point x = {wantedPosition}')
    return start_index, end_index



def getValueAtPosition(quantity_arr, position_arr, wantedPosition):
    """
    Get value at given position.
    If the position does not match any of array elements due to inconsistent gridding, interpolate array and return the value at wanted position.
    """
    if len(quantity_arr) != len(position_arr):
        raise ValueError('Array size does not match!')

    start_idx, end_idx = findCell(position_arr, wantedPosition)

    # linear interpolation
    x_start = position_arr[start_idx]
    x_end   = position_arr[end_idx]
    y_start = quantity_arr[start_idx]
    y_end   = quantity_arr[end_idx]
    tangent = (y_end - y_start) / (x_end - x_start)
    return tangent * (wantedPosition - x_start) + y_start




# -------------------------------------------------------
# Plotting
# -------------------------------------------------------


def getRowColumnForDisplay(num_elements):
    """
    Determine arrangement of multiple plots in one sheet.

    INPUT:
        number of plots

    RETURN:
        number of rows
        number of columns
        (which satisfy number of rows <= number of columns)
    """
    import math
    n = num_elements

    # if not n % 2 == 0: n = n+1   # avoid failure of display when n is odd
    num_rows = 1
    num_columns = int(n)

    if n < 4: return num_rows, num_columns

    while (float(num_rows) / float(num_columns) < 0.7):   # try to make it as square as possible
        k = math.floor(math.sqrt(n))

        while not n % k == 0: k = k-1
        num_rows    = int(k)
        num_columns = int(n / k)
        n = n + 1

    return num_rows, num_columns



def get_maximum_points(quantity_arr, position_arr):
    if len(quantity_arr) != len(position_arr):
        raise ValueError('Array size does not match!')
    ymax = np.amax(quantity_arr)
    xmaxIndex = np.where(quantity_arr == ymax)[0]
    xmax = position_arr[xmaxIndex.item(0)]             # type(xmaxIndex.item(0)) is 'int'
    return xmax, ymax



def generateColorscale(colormap, minValue, maxValue):
    """
    Generate a color scale with given colormap and range of values.
    """
    return plt.cm.ScalarMappable( cmap=colormap, norm=plt.Normalize(vmin=minValue, vmax=maxValue) )



def mask_part_of_array(arr, string='flat', tolerance=1e-4, cut_range=[]):
    """
    Mask some elements in an array to plot limited part of data.

    INPUT:
        arr           data array to be masked
        string        specify mask method. 'flat' masks flat part of the data, while 'range' masks the part specified by the index range.
        tolerance     for 'flat' mask method
        cut_range     list: range of index to define indies to be masked

    RETURN:
        masked array

    """
    if not isinstance(arr, np.ndarray):
        raise TypeError('Given array is not numpy.ndarray')

    arr_size = len(arr)
    maskList = [0 for i in range(arr_size)]
    new_arr = np.ma.array(arr, mask = maskList)   # non-masked np.ma.array with given data arr

    if string == 'flat':
        for i in range(arr_size):
            if i == 0 or i == arr_size-1:  continue

            # check nearest neighbours
            flat_before = np.abs(arr[i] - arr[i-1]) < tolerance
            flat_after = np.abs(arr[i] - arr[i+1]) < tolerance

            if i == 1 or i == arr_size-2:
                if flat_before and flat_after:
                    new_arr.mask[i] = True
                continue

            # check next nearest neighbours
            flat_nextNearest = np.abs(arr[i] - arr[i-2]) < tolerance and np.abs(arr[i] - arr[i+2]) < tolerance

            if flat_before and flat_after and flat_nextNearest:
                new_arr.mask[i] = True

    if string == 'range':
        if cut_range == []: raise NextnanopyScriptError('Specify the range to cut!')

        cut_indices = np.arange(cut_range[0], cut_range[1], 1)
        for i in cut_indices:
            new_arr.mask[i] = True

    return new_arr



def getPlotTitle(originalTitle):
    """
    If the title is too long for display, omit the intermediate letters
    """
    title = separateFileExtension(originalTitle)[0]   # remove extension if present

    if len(title) > 25:
        beginning = title[:10]
        last  = title[-10:]
        title = beginning + ' ... ' + last

    return title



def export_figs(figFilename, figFormat, software, outputSubfolderName='', output_folder_path='', fig=None):
    """
    Export all the matplotlib.pyplot objects in multi-page PDF file or other image formats with a given file name.

    Parameters
    ----------
    figFilename : str
        file name of the exported figure
    figFormat : str
        PDF = vector graphic
        PNG = high quality, lossless compression, large size (recommended)
        JPG = lower quality, lossy compression, small size (not recommended)
        SVG = supports animations and image editing for e.g. Adobe Illustrator
    software : str
        nextnano solver
    outputSubfolderName : str, optional
        subfolder name in the output directory specified in the config, in which the file is saved.
        The default is ''.
    output_folder_path : str, optional
        If present, the file will be saved to this path and outputSubfolderName will be ignored.
        The default is ''.
    fig : matplotlib.subplot object, optional
        Needed if non-PDF format is desired. The default is None.

    Returns
    -------
    None.

    NOTE:
        fig, ax = plt.subplots() must exist, i.e. subplot object(s) must be instantiated before calling this method
        specify image format in the argument of this function if non-PDF format is desired.
        PNG and other non-PDF formats cannot generate multiple pages and ends up with one plot when multiple subplots instances exist.

    """
    # validate arguments
    if figFormat == '.pdf' or figFormat == 'pdf' or figFormat == 'PDF':
        figFormat == '.pdf'
    elif figFormat == '.png' or figFormat == 'png' or figFormat == 'PNG':
        figFormat == '.png'
    elif figFormat == '.jpg' or figFormat == 'jpg' or figFormat == 'JPG':
        figFormat == '.jpg'
    elif figFormat == '.svg' or figFormat == 'svg' or figFormat == 'SVG':
        figFormat == '.svg'
    else:
        raise ValueError("Non-supported figure format!")

    if fig == None and not figFormat == '.pdf':
        raise NextnanopyScriptError("Argument 'fig' must be specified to export non-PDF images!")

    if isinstance(fig, list) and len(fig) > 1 and not figFormat == '.pdf':
        raise NextnanopyScriptError("Non-PDF formats cannot generate multiple pages.")

    # prepare output subfolder path
    if output_folder_path:
        outputSubfolder = output_folder_path
    else:
        outputSubfolderName = separateFileExtension(outputSubfolderName)[0]   # chop off file extension if any
        outputSubfolder = os.path.join(nn.config.get(software, 'outputdirectory'), outputSubfolderName)

    mkdir_if_not_exist(outputSubfolder)
    print(f'\nExporting figure to: {outputSubfolder}\n')

    if figFormat == '.pdf':
        PDF_path = os.path.join(outputSubfolder, figFilename + '.pdf')
        with backendPDF.PdfPages(PDF_path, False) as pdf:
            for figure in range(1, plt.gcf().number + 1):
                pdf.savefig(figure)
    else:
        fig.savefig(os.path.join(outputSubfolder, figFilename + figFormat))


