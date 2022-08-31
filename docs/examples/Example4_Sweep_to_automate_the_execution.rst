Example 4. Use Sweep to automate the execution
==============================================

About this example: Sweep class
-------------------------------

Sweep allows you to automatically create input files with different
values of specific variables.

To work with a sweep, instantiate a Sweep class object as

.. code:: python

   my_sweep = nextnanopy.Sweep(sweep_variables, path_to_inputfile)

Here sweep_variables should be a dict, where keys are the names of
variables and the values are iterable objects of values. (ideally lists)

.. code:: python

   sweep_variables = {'varname1':[val0,val1,val2...],'varname2':[val10,val11,val12...]...}

The name of variables to sweep should coincide with the names of
variables in input file (see Example1).

.. code:: ipython3

    import nextnanopy as nn
    
    path = r'.\input_files/sweep_example.in'
    my_sweep = nn.Sweep({'ALLOY':[0.3,0.6], 'SIZE':[80,100]}, path)
    print(my_sweep)


.. parsed-literal::

    Sweep
    fullpath: .\input_files/sweep_example.in
    Input variables: 8 elements
    	$BIAS = 0.0 # Gate voltage(V)
    	$ALLOY = 0.3 # Al content of AlGaAs layer
    	$SIZE = 80 # size of AlGaAs layer (nm)
    	$DOPECONC = 3e+18 # donor concentration of 10nm doping layer (cm^-3)
    	$DOPEPOS = 65 # distance between AlGaAs-GaAs interface and delta doping position (nm)
    	$MINGRID = 0.1 # minimum grid spacing (nm)
    	$NUMEV = 10 # number of eigenvalues to be calculated
    	$BARRIER = 0.7 # height of left Schottky barrier (eV)
    

To save a sweep, use

.. code:: ipython3

    my_sweep.save_sweep()

After saving, input files are created in the directory of the initial
input file. One can access info about the input files via

.. code:: ipython3

    my_sweep.input_files




.. parsed-literal::

    [InputFile
     fullpath: .\input_files\sweep_example__ALLOY_0.3_SIZE_80_.in
     Input variables: 8 elements
     	$BIAS = 0.0 # Gate voltage(V)
     	$ALLOY = 0.3 # THIS VARIABLE IS UNDER SWEEP
     	$SIZE = 80 # THIS VARIABLE IS UNDER SWEEP
     	$DOPECONC = 3e+18 # donor concentration of 10nm doping layer (cm^-3)
     	$DOPEPOS = 65 # distance between AlGaAs-GaAs interface and delta doping position (nm)
     	$MINGRID = 0.1 # minimum grid spacing (nm)
     	$NUMEV = 10 # number of eigenvalues to be calculated
     	$BARRIER = 0.7 # height of left Schottky barrier (eV),
     InputFile
     fullpath: .\input_files\sweep_example__ALLOY_0.3_SIZE_100_.in
     Input variables: 8 elements
     	$BIAS = 0.0 # Gate voltage(V)
     	$ALLOY = 0.3 # THIS VARIABLE IS UNDER SWEEP
     	$SIZE = 100 # THIS VARIABLE IS UNDER SWEEP
     	$DOPECONC = 3e+18 # donor concentration of 10nm doping layer (cm^-3)
     	$DOPEPOS = 65 # distance between AlGaAs-GaAs interface and delta doping position (nm)
     	$MINGRID = 0.1 # minimum grid spacing (nm)
     	$NUMEV = 10 # number of eigenvalues to be calculated
     	$BARRIER = 0.7 # height of left Schottky barrier (eV),
     InputFile
     fullpath: .\input_files\sweep_example__ALLOY_0.6_SIZE_80_.in
     Input variables: 8 elements
     	$BIAS = 0.0 # Gate voltage(V)
     	$ALLOY = 0.6 # THIS VARIABLE IS UNDER SWEEP
     	$SIZE = 80 # THIS VARIABLE IS UNDER SWEEP
     	$DOPECONC = 3e+18 # donor concentration of 10nm doping layer (cm^-3)
     	$DOPEPOS = 65 # distance between AlGaAs-GaAs interface and delta doping position (nm)
     	$MINGRID = 0.1 # minimum grid spacing (nm)
     	$NUMEV = 10 # number of eigenvalues to be calculated
     	$BARRIER = 0.7 # height of left Schottky barrier (eV),
     InputFile
     fullpath: .\input_files\sweep_example__ALLOY_0.6_SIZE_100_.in
     Input variables: 8 elements
     	$BIAS = 0.0 # Gate voltage(V)
     	$ALLOY = 0.6 # THIS VARIABLE IS UNDER SWEEP
     	$SIZE = 100 # THIS VARIABLE IS UNDER SWEEP
     	$DOPECONC = 3e+18 # donor concentration of 10nm doping layer (cm^-3)
     	$DOPEPOS = 65 # distance between AlGaAs-GaAs interface and delta doping position (nm)
     	$MINGRID = 0.1 # minimum grid spacing (nm)
     	$NUMEV = 10 # number of eigenvalues to be calculated
     	$BARRIER = 0.7 # height of left Schottky barrier (eV)]



To execute the sweep, run

.. code:: python

   Sweep.execute_sweep()

Under execution, a few things will happen. 1. The directory
inputfilename_sweep_var1_var2_…varn will be created in the output
directory. 2. The sweep.info file with the information of the sweep is
saved there. 3. Input files from sweep.input_files are executed and
output is saved to the mentioned folder.

Sweep.execute() has 5 optional parameters + can take any parameter
accepted by nextnanopy.InputFile.execute().

1. delete_input_files: bool, optional

When set to ``True``, input_files will be deleted after execution.
Default is ``False``.

2. overwrite: bool, optional

When set to ``True``, the output will overwrite the old output. When
``False``, execution will create new output folder (with the unique
name, created by adding an integer to the foldername). Default is
``False``.

3. show_log: bool, optional

When set to ``True``, the simulation log is displayed in the console,
while ``False`` suppresses the log. Default is ``True``. Note that the
log file is always saved in the output folders regardless of this
option.

4. convergenceCheck: bool, optional

When set to ``True``, nextnanopy scans the log file of the simulation
performed and check whether the solution has converged. If it did not
converge, nextnanopy warns you and ask if you want to proceed with
postprocessing. Note that non-converged solutions are not reliable and
further calculation and/or visualization from them do not make much
sense. Default is ``False``.

5. parallel_limit: int, optional

number of simulation to run simultaniously. Espicially usefull for
simple simulations which migh be more efficiently rn in parallel. Be
aware that some nextnano solvers parallelize computations internally in
threads (controlled by –threads in nextnanopy config). To avoid
unexpected behaviour and not desirable decrease of simulation speed use
the rule: parallel_limit*threads<= number of physical cores of the
mahcine default parallel_limit = 1

\**kwags Any other parameter accepted by nextnanopy.InputFile.execute()
e.g. exe, license, database, outputdirectory

Example of the simulation in parallel (2 Input files at a time)

.. code:: ipython3

    my_sweep.execute_sweep(delete_input_files = True, overwrite = True, show_log = False, convergenceCheck = True, parallel_limit = 2)


.. parsed-literal::

    
    Remaining simulations in the queue:  3
    
    Remaining simulations in the queue:  2
    
    Remaining simulations in the queue:  1
    
    Remaining simulations in the queue:  0
    
    Waiting queue is empty, all execution and logging are finished
    

Example of the simulation in sequence (if you want to run the sweep
which was already executed, save it one more time)

.. code:: ipython3

    my_sweep.save_sweep(delete_old_files = False)
    my_sweep.execute_sweep(delete_input_files = True, overwrite = True, show_log = False, convergenceCheck = True, parallel_limit = 1)


.. parsed-literal::

    
    Executing simulations [1/4]...
    
    Executing simulations [2/4]...
    
    Executing simulations [3/4]...
    
    Executing simulations [4/4]...
    

Please contact python@nextnano.com for any issues with this document.
