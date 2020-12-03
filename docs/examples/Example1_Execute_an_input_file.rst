Example 1 - Execute an input file
=================================

About this example: load and execute an input file
--------------------------------------------------

To work with an input file, simply do:

.. code:: python

   my_input = nextnanopy.InputFile(path_to_file)

This object contains all the relevant information of the input file such
as the raw text, the variables and the configuration for the execution
(see Example 0).

When you create ``my_input``, the class will first check automatically
the type of the input file (nextnano++, nextnano3, nextnano.NEGF or
nexntano.MSB). Then, it will get the raw text and extract all variables
defined in the file like:

::

   $my_var = 3 # in nextnano++
   %my_var = 3 ! in nextnano3

Note that loading variables or sweeping parameters are not implemented
for nextnano.NEGF nor nextnano.MSB yet.

.. code:: ipython3

    import nextnanopy as nn
    my_input = nn.InputFile(r'..\..\tests\datafiles\nextnano++\example.in')
    print(my_input)


.. parsed-literal::

    InputFile
    fullpath: ..\..\tests\datafiles\nextnano++\example.in
    Input variables: 8 elements
    	$BIAS = 0.0 # Gate voltage(V)
    	$ALLOY = 0.3 # Al content of AlGaAs layer
    	$SIZE = 80 # size of AlGaAs layer (nm)
    	$DOPECONC = 3e+18 # donor concentration of 10nm doping layer (cm^-3)
    	$DOPEPOS = 65 # distance between AlGaAs-GaAs interface and delta doping position (nm)
    	$MINGRID = 0.1 # minimum grid spacing (nm)
    	$NUMEV = 10 # number of eigenvalues to be calculated
    	$BARRIER = 0.7 # height of left Schottky barrier (eV)
    

What information does it contain?
---------------------------------

``my_input`` has the following relevant attributes:

-  fullpath (str): path to the input file including the name
-  text (str): return raw text
-  variables (list): list of InputVariable objects
-  config: nextnano configuration (see Example 0)

.. code:: ipython3

    print(my_input.fullpath)


.. parsed-literal::

    ..\\..\\tests\\datafiles\\nextnano++\\example.in
    

.. code:: ipython3

    my_input.preview()


.. parsed-literal::

    0 # 1D sample for solving quantum-poisson
    1 
    2 #Begin NextnanoWizard parameter section
    3 $BIAS = 0.0 # Gate voltage(V)
    (...)
    135 run{
    136    solve_poisson{}
    137    solve_quantum{}
    138    outer_iteration{} # solve coupled Schrödinger-Poisson equations
    139 }
    140 
    

Input variables
---------------

The input variables are stored in ``my_input.variables`` as a list of
``InputVariable`` objects.

These objects have the following attributes:

-  name (str)
-  value (undefined)
-  unit (str, optional)
-  comment (str, optional)
-  metadata (dict, optional)
-  text (str): raw text in the input file for a given variable

.. code:: ipython3

    print(f"List of variables: {my_input.variables}")


.. parsed-literal::

    List of variables: DictList([
    (index: 0 - key: 'BIAS' - $BIAS = 0.0 # Gate voltage(V)),
    (index: 1 - key: 'ALLOY' - $ALLOY = 0.3 # Al content of AlGaAs layer),
    (index: 2 - key: 'SIZE' - $SIZE = 80 # size of AlGaAs layer (nm)),
    (index: 3 - key: 'DOPECONC' - $DOPECONC = 3e+18 # donor concentration of 10nm doping layer (cm^-3)),
    (index: 4 - key: 'DOPEPOS' - $DOPEPOS = 65 # distance between AlGaAs-GaAs interface and delta doping position (nm)),
    (index: 5 - key: 'MINGRID' - $MINGRID = 0.1 # minimum grid spacing (nm)),
    (index: 6 - key: 'NUMEV' - $NUMEV = 10 # number of eigenvalues to be calculated),
    (index: 7 - key: 'BARRIER' - $BARRIER = 0.7 # height of left Schottky barrier (eV))
    ])
    

Get a variables
~~~~~~~~~~~~~~~

There are several methods to do so:

.. code:: python

   my_input.get_variable(name) # method 1 (recommended)
   my_input.variables[name] # method 2 (recommended)
   my_input[name] # method 3 (recommended)
   my_input.variables[index] # method 4

Let’s have a quick look of the variables in this file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    for var in my_input.variables:
        print(var.text)


.. parsed-literal::

    $BIAS = 0.0 # Gate voltage(V)
    $ALLOY = 0.3 # Al content of AlGaAs layer
    $SIZE = 80 # size of AlGaAs layer (nm)
    $DOPECONC = 3e+18 # donor concentration of 10nm doping layer (cm^-3)
    $DOPEPOS = 65 # distance between AlGaAs-GaAs interface and delta doping position (nm)
    $MINGRID = 0.1 # minimum grid spacing (nm)
    $NUMEV = 10 # number of eigenvalues to be calculated
    $BARRIER = 0.7 # height of left Schottky barrier (eV)
    

Variable line number
~~~~~~~~~~~~~~~~~~~~

It is an information that you won’t probably need, but you can see the
line number in the input file where the variable is defined:

.. code:: python

   my_input.variables['BIAS'].metadata

.. code:: ipython3

    my_input.variables['BIAS'].metadata




.. parsed-literal::

    {'line_idx': 3}



Modify the variable
~~~~~~~~~~~~~~~~~~~

If you want to modify the value of a given variable, you can do:

.. code:: python

   my_input.set_variable('BIAS',value=3)

You can also change the comment:

.. code:: python

   my_input.set_variable('BIAS',comment='this is a new comment')

You can change both at the same time:

.. code:: python

   my_input.set_variable('BIAS',value=3,comment='this is a new comment')

.. code:: ipython3

    print(f"Old variable: {my_input.get_variable('BIAS').text}")
    my_input.set_variable('BIAS',value=3,comment='this is a new comment')
    print(f"New variable: {my_input.get_variable('BIAS').text}")


.. parsed-literal::

    Old variable: $BIAS = 0.0 # Gate voltage(V)
    New variable: $BIAS = 3 # this is a new comment
    

Save the current file
---------------------

``my_input`` has a method ``save`` which allows you to save the current
file.

.. code:: python

   my_input.save()

Note that by default, it won’t overwrite the current file such that it
will find an unused name (like example_1.in) and save it.

You can overwrite the current file:

.. code:: python

   my_input.save(overwrite=True)

You can save it in another location and with another name:

.. code:: python

   my_input.save('new_path\new_input.in')

Automatically, ``my_input.fullpath`` is updated if the saving was
successful.

By default, if the new location does not exist, it will create the
folder automatically. In order to turn this option off, you can do:

.. code:: python

   my_input.save('new_path\new_input.in',automkdir=False)

.. code:: ipython3

    help(my_input.save)


.. parsed-literal::

    Help on method save in module nextnanopy.inputs:
    
    save(fullpath=None, overwrite=False, automkdir=True) method of nextnanopy.inputs.InputFile instance
        Save the current information into a file.
        
        Parameters
        ----------
        fullpath : str, optional
            path including the file name where it will be saved (default is None)
            If None, it will use the current .fullpath
        overwrite : bool, optional
            If it is False, it will find an unused name by adding an extra index like _1
            (default is False)
        automkdir : bool, optional
            If it is True, it will create the folder if it does not exist.
            (default is False)
    
    

Execute the input file
----------------------

In order to execute the input file:

.. code:: python

   my_input.execute()

Note that if you have modified one or more variables, you must save the
file before execution.

The ``execute`` method without any arguments, it will use the
configuration stored in ``my_input.config``. As explained in Example 0,
it will automatically detect the nextnano product (nextnano++,
nextnano3, nextnano.NEGF or nextnano.MSB) and will load the
corresponding configuration parameters prior execution.

.. code:: ipython3

    help(my_input.execute)


.. code-block::

    Help on method execute in module nextnanopy.inputs:
    
    execute(**kwargs) method of nextnanopy.inputs.InputFile instance
        Execute the input file located at .fullpath
        Individual kwargs can be passed like 'license' or 'database'
        If no kwargs is specified, it will use the default values in .config
        
        Parameters
        ----------
        exe : str, optional
            path to executable
        license : str, optional
            path to license file
        database : str, optional
            path to database file
        outputdirectory : str, optional
            path where to save the simulated data
        
        Other parameters can be used depending on the nextnano product.
        For example, 'threads' is accepted for nextnano++.
        Please, see the documentation of the command line arguments for each nextnano product
        in the website (https://www.nextnano.com/)
    
    

.. code:: ipython3

    my_input.execute()


.. parsed-literal::

    ================================================================================
    STARTING...
    ================================================================================
    (...)
    ================================================================================
    DONE.
    ================================================================================


Get information after executing the file
----------------------------------------

The output folder after executing the file is stored at:

.. code:: python

   my_input.folder_output

You can access to all the relevant information from the execution like
the log file location, the command line arguments, etc, via:

.. code:: python

   my_input.execute_info

.. code:: ipython3

    my_input.folder_output


Sweep an input variable
-----------------------

Since you can change the input variable dynamically, you can sweep its
value and execute the file in a simple loop!

.. code:: python

   for value in [0, 1, 2]:
       my_input.set_variable('BIAS',value=value)
       my_input.save() # remember that by default, overwrite is False.
       my_input.execute() 

Change filename and input folder
--------------------------------

If you want to change the current filename or the current input folder,
you can do the following:

.. code:: python

   my_input.filename = 'new_file.in'
   my_input.filename_only = 'new_file' # it will use the original file extension
   my_input.folder_input = 'new_folder'

Please, contact python@nextnano.com for any issue with this example.
