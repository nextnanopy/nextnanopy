# NEXTNANOPY README

[![BSD-3-Clause](https://img.shields.io/github/license/nextnano-GmbH/nextnanopy)](https://opensource.org/licenses/BSD-3-Clause)
[![Downloads](https://img.shields.io/github/downloads/nextnano-GmbH/nextnanopy/total)](https://github.com/nextnano-GmbH/nextnanopy/releases)

nextnanopy is a Python module to interface the [nextnano](https://www.nextnano.com/) software. This package includes features for:

- **Output files**: User-friendly method to load the datafiles which allows easy and flexible post-processing.
- **Input files:** Load input files, set variables, save by finding unused name, execute the file, write input files, etc.
- **Configuration**: Setup default nextnano configuration (path to executables, databases, licenses, etc).
- **Import from GDS files**: Load polygons from GDS files and user-friendly methods to generate raw text of nextnano shapes (beta).

**Note:** A valid license for the nextnano software is not compulsory for the general use of nextnanopy, unless you would like to execute input files via Python.

## Installation

nextnanopy can be installed on Linux / macOS / Windows. It requires Python >= 3.10.

To install the latest release the standard way, run the following in your Python environment of choice:

```bash
pip install nextnanopy
```

Alternatively, if you want the development version (for Python experts only), clone the GitHub repository into a directory of your choice and install it from there:

```bash
git clone https://github.com/nextnano-GmbH/nextnanopy.git
cd nextnanopy
pip install -e .
```

For details, please refer to docs/How to install nextnanopy.md.

## Documentation

Basic features are documented in [docs/examples](docs/examples).
Python scripts in [templates/](templates) will help you to start playing with nextnanopy. 
More advanced scripts for postprocessing/plotting results of nextnano++ simulations are located in examples folder of the nextnano++ distribution.

## Support

Do you want to help nextnanopy? Please send an email to [python@nextnano.com](mailto:python@nextnano.com).

## History of changes

## Development version

<!-- cspell:disable-next-line -->
- the nextnano.NEGF keyword argument `debug_ouptut_specifications` is now spelled `debug_output_specifications`. If you passed the old name, update it: because it reaches the command builder through `**kwargs`, the misspelled name is now accepted and ignored rather than raising, so a stale call silently stops passing `--debug` to the solver.

## Version 1.2.0 (July 20th, 2026)

- `InputFile(text=...)` now builds an input file from a string: the product is detected from the text, the right product class is returned, and the variables are parsed — without reading anything from disk. Previously the text was silently ignored and you got back an empty, product-agnostic object. `InputFile(fullpath, text=...)` does the same and keeps `fullpath` as the name to save back to; it used to raise `TypeError`. Note that `InputFile()` followed by `file.text = ...` cannot work and never could — with no text at construction there is nothing to detect the product from, so you get a product-agnostic object whose `.variables` stays empty. Use `InputFile(text=...)` instead.
- bug fix: `InputFile`'s `parse` argument is no longer ignored when passed positionally. `InputFile(path, None, True)` silently left the file unparsed (`.content` was `None`); only the `InputFile(path, parse=True)` spelling worked. Both now behave the same.
- `InputFile` cannot be subclassed and now says so with a `TypeError`. It chooses the class to build from the file's contents, so a subclass was silently discarded and you got a plain product class back. Subclass the product's `InputFile` (e.g. `nextnanopy.nnp.inputs.InputFile`), or `InputFileTemplate` for all products. Related: `isinstance(InputFile(path), InputFile)` is `False` — the object you get back is a product class, and `InputFileTemplate` is the common base to check against and annotate with.
- introduced `ExecutionPool` (`nextnanopy.inputs`), a `ThreadPoolExecutor`-based alternative to `ExecutionQueue` for running input files concurrently. Not yet used internally (`Sweep` still uses `ExecutionQueue`); available for direct use.
- `Sweep` now has `save()` and `execute()` as the preferred, shorter names for `save_sweep()` and `execute_sweep()`. For now they simply forward to the existing methods, so nothing changes; in a future release the names will swap (the short names will hold the implementation and the `*_sweep` names will remain as deprecated aliases). Prefer `sweep.save()` / `sweep.execute()` in new code.
- convergence check no longer hangs headless runs: `check_convergence(mode='pause')` asks how to proceed only when an interactive terminal is attached; without one (CI, cluster jobs) it now raises like `mode='terminate'` instead of blocking on input.
- `nextnanopy.config.set(...)` now reaches every input file you create afterwards, with no `save()` needed — configure first, then build your input files. Previously a `set()` was ignored unless it was followed by `save()`. The configuration is bound when the input file is created: it takes a copy of `nextnanopy.config` as it stands at that moment, so later changes to `nextnanopy.config` do not reach files that already exist, and editing `file.config` changes neither `nextnanopy.config` nor any other input file. The input files a `Sweep` generates follow the same rule. Passing `configpath` still takes precedence over all of this.
- importing `nextnanopy` no longer creates or checks `~/.nextnanopy-config`. The config is built on first access of `nextnanopy.config` (or when an `InputFile` is created without `configpath`).
- saving the config file is now atomic: an interrupted write can no longer leave a half-written `.nextnanopy-config` behind.
- `Config` with an empty path now raises `ValueError`; a path to a non-existing file yields an empty configuration that can be filled in and saved.
- bug fix: `ExecutionQueue` no longer busy-spins at 100% CPU while waiting for parallel simulations (`limit_parallel > 1`). It now sleeps between checks (`ExecutionQueue.poll_interval`, default 0.1 s) and fills all free parallel slots at once; wall time is unchanged.
- performance: creating an `InputFile` reads the file (and sets up the config) only once; product detection loads the file once instead of once per product; `DataFile` loads the data from disk only once (product-specific `.txt` files still need two reads).
- `DataFile` restructured: the per-product `DataFile` classes are removed, only per-product `.txt` loaders remain. Loader autodetection now raises `NotImplementedError` with a clear message when no loader fits.
- removed `nextnanopy.defaults.get_DataFile`, which mapped a product name to its `DataFile` class. Use `nextnanopy.DataFile(path, product=...)` instead.
- `execute` is no longer exported at the top level: `nextnanopy.execute` is gone. It was the low-level command runner, which requires `exe`, `license`, `database` and `outputdirectory` to be passed by hand — the very things nextnanopy reads from your configuration for you. Use `InputFile.execute()` (as in all the examples), or import `nextnanopy.commands.execute` directly if you really want the raw call.
- `nextnanopy.commands.execute` now raises a clear `ValueError` for an empty or non-existing input file path before starting a simulation.
- bug fix: nested or concurrent loops over the same `DictList`, `InputFile` or `DataFile` no longer interfere with each other. Iterating the same object in an inner and an outer loop (e.g. `for v1 in datafile: for v2 in datafile: ...`) used to end the outer loop early, because the iteration position was stored on the object itself. Iteration still yields the values (`Variable`/`Coord` objects, input variables), so no API change.
- bug fix: the detected product for invalid input files is consistently lowercase `'not valid'`
- bug fix: replaced deprecated `xml` usage in nextnano.NEGF_classic input handling
- removed the unused `is_{product}_input_file` functions (superseded by `is_{product}_input_text`)
- internal: `savetxt` in `utils/misc` refactored; first unit tests for `ExecutionQueue` added and sped up; nextnano++ syntax updated in the test example input file

## Version 1.1.1 (July 13th, 2026)
- bugfixes
- enforce ruff linting and formatting

## Version 1.1.0 (May 5th, 2026)
- most of the templates are moved to the nextnano tools distribution packages, no longer part of this repo
- new parameter `parse` for `InputFile` (default `False`): content parsing of nextnano++ input files is now opt-in. Use `InputFile(fullpath, parse=True)` to populate `file.content` with the block structure. With the default `parse=False` the file loads normally — variables are available, `content` is `None` — which also allows loading files where preprocessor directives cause unbalanced `{}` that the parser cannot handle.
- bugfixes

## Version 1.0.5 (Mar 24th, 2026)

- bugfix

## Version 1.0.4 (Mar 24th, 2026)

- saving sweeps in temporary location: Sweep.save_sweep(temp=True)
- bugfix with json output file of the sweep
- templates updates

### Version 1.0.3 (Jan 8th, 2026)

- now modern MSB input files are supported
- use dandelion instead of golden in plotting pallette 
- enforce alphabetical order in DataFolder tree 

### Version 1.0.2 (Oct 10th, 2025)

- bugfix: now supports the avs binary files with ascii coords
- added nextnano mpl style for plotting, see utils
- added possibility to save input files in temporary folder: InputFile.save(temp=True)
- improved gds import

### Version 1.0.1 (Jul 12th, 2025)

- .txt files are read as Dat without coords (all columns are variables)

### Version 1.0.0 (Jul 11th, 2025)

- support of python3.13
- NEGF renamed to NEGF_classic (requires .nextnanopy-config update)
- NEGF++ renamed to NEGF (requires .nextnanopy-config update)

### Version 0.1.22 (May 7th, 2024)

- improved Dat loader

### Version 0.1.21 (Feb 28th, 2024)

- Added DataFile loader for total_charges.txt
- nextnanopy now supports python3.11

### Version 0.1.20 (Dec 13th, 2023)

- nextnanopy is aligned to be used with nextnanoevo. nextnanoevo will be released in 2024

### Version 0.1.19 (Jul 21st, 2023)

- new feature: saving DataFile: DataFile.save
- new feature: DataFolder.find_multiple - search files by multiple keywords
- new property DataFolder.name - return the basename of the folder

### Version 0.1.18 (Jul 04th, 2023)

- new product available: nextnano.NEGF++
- setting the text for InputFile is available again (but switching product when setting text os forbidden)
- interface with .gds files is extended

### Version 0.1.17 (Jun 07th, 2023)

- fixed a bug with nnp.shapes.GdsPolygons.get_obelisks
- get_obelisks can be used again. The usage is deprecated, nnp.shapes.GdsPolygons.get_polygonal_prisms is preferred way to convert gds to nextnano++ structure

### Version 0.1.16 (Apr 25th, 2023)

- nextnanopy now supports python 3.10!
- The execute_sweep function has been updated to include a new parameter, separate_sweep_dir, which allows the user to specify whether the output files should be saved in a separate directory or a common output directory.
  By default, execute_sweep will still create a separate output directory for each sweep. However, if the user sets separate_sweep_dir to False, the output files will be saved in a common output directory instead.
- ListDict now supports negative indexes (in the same way as a normal python list)
- nnpp assistant is updated
- shapely is no longer necessary to import geometry from gdsii file

### Version 0.1.15 (Aug 31st, 2022)

- input files now can be executed in parallel through nextnanopy.inputs.ExecutionQueue class
- Sweep uses ExecutionQueue and executes several simulations in parallel if parallel_limit>1 in Sweep.execute_sweep(parallel_limit = n)

### Version 0.1.14 (Jul 27th, 2022)

- nextnanopy.Sweep.save_sweep has parameter round_decimal to limit round of digits in the folder names. Default round_decimal = 8

### Version 0.1.13 (Jun 13th, 2022)

- Default .dat loader of nextnanopy.DataFile was changed. Before x,y,z and position were coordinates, anything else recognized as variables. Now first column of the '.dat' file is recognized as coordinate, all other columns are variables.
- Demo: parser of the whole input file for nextnano++. Raise error if file contains incorrect number and order of parentheses '{}'

### Version 0.1.12 (Mar 14th, 2022)

- added support of input variables for nextnanoNEGF. Note: after save all non-xml data (i.e. comments) is not preserved.

### Version 0.1.11 (Jan 10th, 2022)

- Feature: DataFile.plot() - make a preview plot. Graph for 1-dimensional data and a colormap for 2-dimensional data.
- Feature: New class DataFolder. Designed to simplify navigation in output directory.
- Beta feature: postprocess.simple_optimize. Runs simulation over given variables space and optimizes the desired output value.

### Version 0.1.10 (Oct 06th, 2021)

- Feature: Added new class Sweep allowing to create automatic sweeps over few variables

### Version 0.1.9 (Dec 16th, 2020)

- Feature: InputFile.execute has now show_log (True or False) to turn on/off the log. Note: the log file is always saved.
- Removed default messages when saving an input file

### Version 0.1.8 (Dec 14th, 2020)

- Buf fix: find unused name when saving input file

### Version 0.1.7 (Dec 3rd, 2020)

- docstring for inputs.py, outputs.py, config.py, mycollections.py, datasets.py
- Updated examples in docs/examples/

### Version 0.1.6 (Dec 2nd, 2020)

- Feature: [DataFile] access with index to coordinates and to variables

```python
df = nextnanopy.DataFile(...)
df['x'] # same as df.coords['x']
df['Gamma'] # same as df.variables['Gamma']
```

- Feature: [DataFile] is loopable as well as .coords and .variables
- Feature: [InputFile] access with index to input variables

```python
df = nextnanopy.InputFile(...)
df['xmax'] # same as df.variables['xmax']
```

- Feature: [InputFile] is loopable as well as .coords and .variables
- Feature: [InputFile] extra attributes

```python
df = nextnanopy.InputFile(...)
df.folder_output # returns the output folder if it was executed, otherwise it raises an error
df.filename      # settable
df.filename_only # settable
df.folder_input  # settable
```

- Feature: User-friendly information for DataFile, InputFile, Variable, Coord and InputVariable
- Bug fix: .vtr dataset reshape method

### Version 0.1.5 (Dec 2nd, 2020)

- Feature: Support of .vtr data files
- Feature: If unit is not found, default value is 'a.u.'.
- Bug fix: Better methods to find correctly name and unit from data file headers

### Version 0.1.4 (Nov 29th, 2020)

- Feature: Create an empty input file and set the raw text with the attribute text.

### Version 0.1.3 (Nov 28th, 2020)

- Bug fix: Find unused name when save input files.
- Feature: Default label for Variables and Coords. The attribute label returns "name (unit)".

### Version 0.1.2 (Nov 20th, 2020)

- Bug fix: Raw text of input variables without comment was generated incorrectly.

### Version 0.1.1 (Nov 18th, 2020)

- Bug fix: Find the home path for OSX and Linux.

### Version 0.1.0 (Nov 13th, 2020)

- Initial release
