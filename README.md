# NEXTNANOPY README

[![BSD-3-Clause](https://img.shields.io/github/license/nextnanopy/nextnanopy)](https://opensource.org/licenses/BSD-3-Clause)
[![Downloads](https://img.shields.io/github/downloads/nextnanopy/nextnanopy/total)](https://github.com/nextnanopy/nextnanopy/releases)

nextnanopy is a Python module to interface the [nextnano](https://www.nextnano.com/) software. This package includes features for:
* **Output files**: user-friendly method to load the datafiles which allows easy and flexible post-processing. 
* **Input files:** load input files, set variables, save by finding unused name, execute the file, write input files, etc.
* **Configuration**: setup default nextnano configuration (path to executables, databases, licenses, etc).
* **Import from GDS files**: load polygons from GDS files and user-friendly methods to generate raw text of nextnano shapes (beta).

**Note:** the license is not compulsory for the general use of nextnanopy, unless you would like to execute input files via Python.

## Future of nextnanopy
Currently, nextnanopy has basic features for [nextnano products](https://www.nextnano.com/products/products.php) nextnano++, nextnano3, nextnano.NEGF and nextnano/MSB. The goal is to extend the functionalities to nextnano.MSB in future releases.

In future releases, we would like to implement:

* **Common post-processing methods**: like loading and plotting together bandedges, eigenenergies and eigenlevels, colormap of potential landscape with GDS polygons on top, etc.
* **Support for any nextnano.NEGF datafiles**: in the current release, it is only implemented the loading of .dat files (most of them).
* **Support for any nextnano.MSB datafiles**: not loading routines are implemented yet.
* **User-friendly input file creation/modification**: the idea is to load any input file and it would detect all the different blocks so the user can easily modify parameters like 'boundary conditions' or 'region material'. Similarly, it should be user-friendly to create any input file from scratch via Python.
* **Feedback loops**: a routine that allows the user to optimize any figure of merit of a device with a given set of input variables. The user can set a post-processing routine to get the figure of merit from the simulated data and later, a new set of input variables will be generated and executed. This feedback loop will repeat until a set of conditions are satisfied.
* **Improve documentation**: we will add an extensive documentation in the website as well as in the source code.
* **Guidelines for contributors**: set of rules if you want to contribute to the project.
 
## Installation

### Requirements

You need a working python 3.x installation to be able to use nextnanopy. We highly recommend installing [Anaconda](https://www.anaconda.com/), which takes care of installing Python and managing packages. 
Make sure to download the latest version with python 3.8.

### Dependencies:

* [Python](https://www.python.org/) (tested with 3.8)
* [Numpy](http://numpy.scipy.org/)
* [Gdspy](https://gdspy.readthedocs.io/) (optional: to import gds files)
* [Shapely](https://shapely.readthedocs.io/) (optional: to manipulate polygons from gds files)
* [Matplotlib](https://matplotlib.org/) (optional: to visualize imported polygons)
* [Cylcer](https://pypi.org/project/Cycler/) (optional: to visualize imported polygons)

### Linux / OS X / Windows

#### Option 1: Using [pip](https://docs.python.org/3/installing/)

Simply open anaconda prompt and type:

```sh
pip install nextnanopy
```

#### Option 2: from the source code

1. Download the source from [github](https://github.com/nextnanopy/nextnanopy)
2. Open anaconda prompt
3. Go to the directory of the nextnanopy project
4. Build/install by typing:

```sh
python setup.py install
```

For more information, please, see the documents in docs folder.

## Documentation

Currently, the complete documentation is not available yet. However, there are few examples located in docs/examples that will help you to start playing with nextnanopy.


## Support

Do you want to help nextnanopy? Please, send an email to [python@nextnano.com](mailto:python@nextnano.com). 


## History of changes

### Upcoming
* Detailed documentation

### Version 0.1.4 (Nov 29th, 2020)
* Feature: create an empty input file and set the raw text with the attribute text.

### Version 0.1.3 (Nov 28th, 2020)
* Bug fix: find unused name when save input files
* Feature: default label for Variables and Coords. The attribute label returns "name (unit)". 

### Version 0.1.2 (Nov 20th, 2020)
* Bug fix: Raw text of input variables without comment was generated incorrectly

### Version 0.1.1 (Nov 18th, 2020)
* Bug fix: find the home path for OSX and Linux. 

### Version 0.1.0 (Nov 13th, 2020)
* Initial release.
