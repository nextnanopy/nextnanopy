# NEXTNANOPY README

[![BSD-3-Clause](https://img.shields.io/**)](https://opensource.org/licenses/BSD-3-Clause)
[![Documentation Status](https://readthedocs.org/**)](https://gdspy.readthedocs.io/**)
[![Appveyor Status](https://ci.appveyor.com/**)](https://ci.appveyor.com/**)
[![Downloads](https://img.shields.io/**)](https://github.com/**/releases)

nextnanopy is a Python module to interface the [nextnano](https://www.nextnano.com/) software. This package includes features for:
* **Input files:** load input files, set variables, save by finding unused name, execute the file, write input files, etc.
* **Output files**: user-friendly method to load the datafiles which allows easy and flexible post-processing.
* **Import from GDS files**: load polygons from GDS files and user-friendly methods to generate raw text of nextnano shapes (beta).



## Future of nextnanopy
Currently, it only supports files and features from nextnano++ and nextnano3, although the goal is to extend the functionalities to nextnano.NEGF and nextnano.MSB in future releases.

On the other hand, the helper for the creation of input files will be improved as well as the generation of nextnano shapes. 
 
## Installation

### Dependencies:

* [Python](https://www.python.org/) (tested with 3.8)
* [Numpy](http://numpy.scipy.org/)
* [Gdspy](https://gdspy.readthedocs.io/) (optional: to import gds files)
* [Shapely](https://shapely.readthedocs.io/) (optional: to manipulate polygons from gds files)
* [Matplotlib](https://matplotlib.org/) (optional: to visualize imported polygons)
* [Cylcer](https://pypi.org/project/Cycler/) (optional: to visualize imported polygons)

### Linux / OS X / Windows

Option 1: using [pip](https://docs.python.org/3/installing/):

```sh
pip install nextnanopy
```

Option 2: download the source from [github (LINK HERE!!)](https://github.com/**) and build/install with:

```sh
python setup.py install
```

## Documentation

The complete documentation is available [here (LINK HERE!!)](http://**).


## Support

Help support nextnanopy development by [donating via PayPal (link??)](https://**)


## History of changes

### Upcoming
* Detailed documentation


### Version 0.1.0 (**, 2020)
* Initial release.
