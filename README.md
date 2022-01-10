# NEXTNANOPY README

[![BSD-3-Clause](https://img.shields.io/github/license/nextnanopy/nextnanopy)](https://opensource.org/licenses/BSD-3-Clause)
[![Downloads](https://img.shields.io/github/downloads/nextnanopy/nextnanopy/total)](https://github.com/nextnanopy/nextnanopy/releases)

nextnanopy is a Python module to interface the [nextnano](https://www.nextnano.com/) software. This package includes features for:
* **Output files**: User-friendly method to load the datafiles which allows easy and flexible post-processing. 
* **Input files:** Load input files, set variables, save by finding unused name, execute the file, write input files, etc.
* **Configuration**: Setup default nextnano configuration (path to executables, databases, licenses, etc).
* **Import from GDS files**: Load polygons from GDS files and user-friendly methods to generate raw text of nextnano shapes (beta).

**Note:** A valid license for the nextnano software is not compulsory for the general use of nextnanopy, unless you would like to execute input files via Python.

## Future of nextnanopy
Currently, nextnanopy has basic features for [nextnano products](https://www.nextnano.com/products/products.php) nextnano++, nextnano³, nextnano.NEGF and nextnano.MSB.

In future releases, we would like to implement:

* **Common post-processing methods**: Like loading and plotting together bandedges, eigenenergies and eigenlevels, colormap of potential landscape with GDS polygons on top, etc.
* **Improved support for specific nextnano.NEGF and nextnano.MSB datafiles**
* **User-friendly input file creation/modification**: The idea is to load any input file and it would detect all the different blocks so the user can easily modify parameters like 'boundary conditions' or 'region material'. Similarly, it should be user-friendly to create any input file from scratch via Python.
* **Feedback loops**: A routine that allows the user to optimize any figure of merit of a device with a given set of input variables. The user can set a post-processing routine to get the figure of merit from the simulated data and later, a new set of input variables will be generated and executed. This feedback loop will repeat until a set of conditions are satisfied.
* **Improve documentation**: We will add an extensive documentation in the website as well as in the source code.
* **Guidelines for contributors**: Set of rules if you want to contribute to the project.
 
## Installation

### Requirements

You need a working Python 3.8 installation to be able to use nextnanopy. We highly recommend installing [Anaconda](https://www.anaconda.com/), which takes care of installing Python and managing packages. 
Make sure to download the latest version with Python 3.8.

### Dependencies:

* [Python](https://www.python.org/) (tested with 3.8)
* [NumPy](http://numpy.scipy.org/)
* [PyVista](https://www.pyvista.org/) (For loading VTK files)
* [Gdspy](https://gdspy.readthedocs.io/) (optional: to import gds files)
* [Shapely](https://shapely.readthedocs.io/) (optional: to manipulate polygons from gds files)
* [Matplotlib](https://matplotlib.org/) (optional: to visualize imported polygons)
* [Cycler](https://pypi.org/project/Cycler/) (optional: to visualize imported polygons)

### Linux / OS X / Windows

#### Option 1: Using [pip](https://docs.python.org/3/installing/)

Simply open Anaconda prompt and type:

```sh
pip install nextnanopy
```
or if you want to upgrade:
```sh
pip install --upgrade nextnanopy
```

#### Option 2: From the source code

1. Download the source from [github](https://github.com/nextnanopy/nextnanopy)
2. Open Anaconda prompt
3. Go to the directory of the nextnanopy project
4. Build/install by typing:

```sh
python setup.py install
```

For more information, please see the documents in docs/ folder.

## Documentation

Currently, the complete documentation is not available yet. However, there are few examples located in templates/ and docs/examples that will help you to start playing with nextnanopy.


## Support

Do you want to help nextnanopy? Please, send an email to [python@nextnano.com](mailto:python@nextnano.com). 


## History of changes


### Version 0.1.11 (Jan 10th, 2022)
* Feature: DataFile.plot() - make a preview plot. Graph for 1-dimensional data and a coplormap for 2-dimensional data.
* Feature: New class DataFolder. Designed to simplify navigation in output directory.
* Beta feature: postprocess.simple_optimize. Runs simulation over given variables space and optimizes the desired output value.


### Version 0.1.10 (Oct 06th, 2021)
* Feature: Added new class Sweep allowing to create automatic sweeps over few variables 


### Version 0.1.9 (Dec 16th, 2020)
* Feature: InputFile.execute has now show_log (True or False) to turn on/off the log. Note: the log file is always saved. 
* Removed default messages when saving an input file

### Version 0.1.8 (Dec 14th, 2020)
* Buf fix: find unused name when saving input file

### Version 0.1.7 (Dec 3rd, 2020)
* docstring for inputs.py, outputs.py, config.py, mycollections.py, datasets.py
* Updated examples in docs/examples/

### Version 0.1.6 (Dec 2nd, 2020)
* Feature: [DataFile] access with index to coordinates and to variables
```python
df = nextnanopy.DataFile(...)
df['x'] # same as df.coords['x']
df['Gamma'] # same as df.variables['Gamma']
```
* Feature: [DataFile] is loopable as well as .coords and .variables
* Feature: [InputFile] access with index to input variables
```python
df = nextnanopy.InputFile(...)
df['xmax'] # same as df.variables['xmax']
```
* Feature: [InputFile] is loopable as well as .coords and .variables
* Feature: [InputFile] extra attributes
```python
df = nextnanopy.InputFile(...)
df.folder_output # returns the output folder if it was executed, otherwise it raises an error
df.filename      # settable
df.filename_only # settable
df.folder_input  # settable
```
* Feature: User-friendly information for DataFile, InputFile, Variable, Coord and InputVariable
* Bug fix: .vtr dataset reshape method

### Version 0.1.5 (Dec 2nd, 2020)
* Feature: Support of .vtr data files
* Feature: If unit is not found, default value is 'a.u.'.
* Bug fix: Better methods to find correctly name and unit from data file headers

### Version 0.1.4 (Nov 29th, 2020)
* Feature: Create an empty input file and set the raw text with the attribute text.

### Version 0.1.3 (Nov 28th, 2020)
* Bug fix: Find unused name when save input files.
* Feature: Default label for Variables and Coords. The attribute label returns "name (unit)". 

### Version 0.1.2 (Nov 20th, 2020)
* Bug fix: Raw text of input variables without comment was generated incorrectly.

### Version 0.1.1 (Nov 18th, 2020)
* Bug fix: Find the home path for OSX and Linux.

### Version 0.1.0 (Nov 13th, 2020)
* Initial release
