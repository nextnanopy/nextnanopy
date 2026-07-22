# How to install nextnanopy
Updated: 2026-07-22

Contact: python@nextnano.com

## Requirements
- Python 3.10 or later (these are the versions we actively test against)
- Works on Linux, macOS and Windows

A valid nextnano license is not required for the general use of nextnanopy —
only if you want to execute input files (run simulations) via Python.

## New to Python? (optional)
If you are new to Python, two things are worth knowing before you start; neither
is specific to nextnanopy, and experienced users can skip this section.

- **Environments.** This is entirely optional — if you are just getting
  started, you can ignore it and run the `pip install` commands below in your
  plain Python installation. That said, it is good practice to install packages
  into an isolated *virtual environment* rather than your system-wide Python, so
  that each project keeps its own set of dependencies. You can create one with
  the built-in [`venv`](https://docs.python.org/3/library/venv.html) module, or
  with a distribution such as [conda](https://docs.conda.io/) if you prefer.
  Activate the environment first, then run the `pip install` commands inside it.
- **Editors.** nextnanopy is a plain Python library, so any editor works. Common
  choices are [VS Code](https://code.visualstudio.com/),
  [JupyterLab](https://jupyter.org/) (good for the example notebooks) and
  [Spyder](https://www.spyder-ide.org/). None of them are required.
- **If the install fails with a "permission denied" error**, try opening your
  terminal with administrator rights and running the command again. This is
  usually only needed when Python lives outside your own user directory (a
  system-wide, all-users installation), where writing to it requires elevated
  permissions. Installing into a per-user Python or a virtual environment avoids
  the problem entirely.

## Option 1: Install the latest release (recommended)
Run the following in your Python environment of choice:
```sh
pip install nextnanopy
```
To upgrade to the latest version later:
```sh
pip install --upgrade nextnanopy
```

## Option 2: Development install from source
Installing from source keeps the `templates/` and `docs/` examples locally and
lets you edit the library and contribute changes back. nextnanopy is an open
repository — contributions are very welcome!

Clone the repository into a directory of your choice, then install it in
editable mode:
```sh
git clone https://github.com/nextnano-GmbH/nextnanopy.git
cd nextnanopy
pip install -e .
```
To upgrade later, pull the latest changes from inside the folder:
```sh
git pull
```

## Optional features
Some features rely on extra packages that are not installed by default. Install
them via the corresponding *extras*:
```sh
pip install "nextnanopy[plot]"   # plotting helpers (DataFile.plot, styles)
pip install "nextnanopy[gds]"    # import shapes from GDS files
pip install "nextnanopy[post]"   # post-processing (CV curves, minimization)
pip install "nextnanopy[all]"    # everything above
```
The same extras work with the editable install, e.g. `pip install -e ".[all]"`.

## Set up the configuration
After installing, follow
[Example 0](https://github.com/nextnano-GmbH/nextnanopy/blob/master/docs/examples/Example0_Set_up_the_configuration.ipynb)
to point nextnanopy at your nextnano executables, databases and license.

## Dependencies
Required (installed automatically):
- [NumPy](https://numpy.org/)
- [PyVista](https://www.pyvista.org/) (to load VTK data)

Optional (installed via the extras above):
- [Matplotlib](https://matplotlib.org/) and [Cycler](https://pypi.org/project/Cycler/) — visualize data (`plot`)
- [gdspy](https://gdspy.readthedocs.io/) and [Shapely](https://shapely.readthedocs.io/) — import and manipulate polygons from GDS files (`gds`)
- [SciPy](https://scipy.org/) — post-processing (`post`)
