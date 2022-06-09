# How to install nextnanopy
Updated: 2022-06-09

Contact: python@nextnano.com

## Requirements
- Python 3.8 or later (recommended installation with [Anaconda](https://www.anaconda.com/products/individual))

Anaconda takes care of installing Python and managing packages and includes Anaconda Prompt, which is like a Command Prompt on Windows or Terminal on Linux/Mac.

If the access is denied during installation, try to open Anaconda Prompt with administrator rights.

## Option 1: Manual installation
The advantage of manual installation is that you have all the templates stored locally, based on which you can immediately start writing your own Python script using nextnanopy library.

Nextnanopy is an open repository; you are very welcome to contribute to further development!

1. Clone the source from [GitHub](https://github.com/nextnanopy/nextnanopy)
2. Open the Anaconda Prompt
3. Go to the directory of the nextnanopy project folder
4. Build nextnanopy by:  
```sh
python setup.py install
```
5. Open Spyder by:  
```sh
spyder
```  
Now you should be able to import nextnanopy library.
6. Follow [Example 0](https://github.com/nextnanopy/nextnanopy/blob/master/docs/examples/Example0_Set_up_the_configuration.ipynb) to set up the configuration

To upgrade to the latest version, from Anaconda Prompt,
1. 'git pull' the repository
2. Build by:  
```sh
python setup.py install
```

## Option 2: Automatic installation
The advantage of automatic installation is that it does not require knowledge of the GitHub repository.
1. Open the Anaconda Prompt
2. Install by:  
```sh
pip install nextnanopy
```
3. Open Spyder by:  
```sh
spyder
```
Now you should be able to import nextnanopy library.
4. Follow [Example 0](https://github.com/nextnanopy/nextnanopy/blob/master/docs/examples/Example0_Set_up_the_configuration.ipynb) to set up the configuration

To upgrade to the latest version, from Anaconda Prompt,  
```sh
pip install --upgrade nextnanopy
```

## Dependencies
Many of these packages come with Anaconda.

Necessary packages:
- [Python](https://www.python.org/) (tested with version 3.8)
- [Numpy](http://numpy.scipy.org/)
- [PyVista](https://www.pyvista.org/) (to load VTK data)

Optional packages to enhance nextnanopy:
- [Matplotlib](https://matplotlib.org/) (to visualize data)
- [Gdspy](https://gdspy.readthedocs.io/) (to import GDS files)
- [Shapely](https://shapely.readthedocs.io/) (to manipulate polygons from GDS files)
- [Cycler](https://pypi.org/project/Cycler/) (to visualize imported polygons)

If any package is missing, you can install from Anaconda Prompt with:  
```sh
conda install <package name>
```
