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
    
    path = r'E:\nextnano Users\heorhii.yehiazarian\nextnanopy\nextnanopy_package\nextnanopy\docs\examples\input_files/sweep_example.in'
    my_sweep = nn.Sweep({'ALLOY':[0.3,0.6], 'SIZE':[80,100]}, path)
    print(my_sweep)


.. parsed-literal::

    Sweep
    fullpath: E:\nextnano Users\heorhii.yehiazarian\nextnanopy\nextnanopy_package\nextnanopy\docs\examples\input_files/sweep_example.in
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
     fullpath: E:\nextnano Users\heorhii.yehiazarian\nextnanopy\nextnanopy_package\nextnanopy\docs\examples\input_files\sweep_example__ALLOY_0.3_SIZE_80_.in
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
     fullpath: E:\nextnano Users\heorhii.yehiazarian\nextnanopy\nextnanopy_package\nextnanopy\docs\examples\input_files\sweep_example__ALLOY_0.3_SIZE_100_.in
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
     fullpath: E:\nextnano Users\heorhii.yehiazarian\nextnanopy\nextnanopy_package\nextnanopy\docs\examples\input_files\sweep_example__ALLOY_0.6_SIZE_80_.in
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
     fullpath: E:\nextnano Users\heorhii.yehiazarian\nextnanopy\nextnanopy_package\nextnanopy\docs\examples\input_files\sweep_example__ALLOY_0.6_SIZE_100_.in
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

Sweep.execute() has 2 optional parameters

1. delete_input_files: bool, optional. When set to True, input_files
   will be deleted after execution. Default value is False
2. overwrite: bool, optional When set to True, the output will overwrite
   the old output. When False, execution will create new output folder
   (with the unique name, created by adding an integer to the
   foldername). Default value is False.

.. code:: ipython3

    my_sweep.execute_sweep(delete_input_files = True)


.. parsed-literal::

    ================================================================================
    STARTING...
    ================================================================================
    Starting execution as:
    C:\Program Files\nextnano\2021_05_10\nextnano++\bin 64bit\nextnano++_Intel_64bit.exe --license C:\Users\heorhii.yehiazarian\Documents\nextnano\License\License_nnp.lic --database C:\Program Files\nextnano\2021_05_10\nextnano++\Syntax\database_nnp.in --threads 0 --outputdirectory E:\nextnano Users\heorhii.yehiazarian\nextnanopy\nextnanopy_output\sweep_example_sweep__ALLOY__SIZE9\sweep_example__ALLOY_0.3_SIZE_80_ --noautooutdir E:\nextnano Users\heorhii.yehiazarian\nextnanopy\nextnanopy_package\nextnanopy\docs\examples\input_files\sweep_example__ALLOY_0.3_SIZE_80_.in 
    
    nextnano++ (1.7.54 - 2021.050601) May 10 2021
    =============================================================================
    COPYRIGHT NOTICE                                                             
    =============================================================================
    Please read the file 'copyright_nextnano++.txt' in your installation folder  
    for further information about the terms of copyright of the nextnano++ code  
    and of third party source codes and libraries used in the nextnano++ code.   
                                                                                 
    In case this file is missing or seems incomplete or corrupted, please contact
    nextnano GmbH, Germany by submitting a support request on www.nextnano.de or 
    by sending an email to support@nextnano.com in order to receive a new copy.  
                                                                                 
    ANY USE OF THE NEXTNANO++ CODE CONSTITUTES ACCEPTANCE OF THE TERMS OF THE    
    COPYRIGHT NOTICE.                                                            
    =============================================================================
    
    
    =============================================================================
     PROCESSING FILE: E:\nextnano Users\heorhii.yehiazarian\nextnanopy\nextnanopy_package\nextnanopy\docs\examples\input_files\sweep_example__ALLOY_0.3_SIZE_80_.in
    =============================================================================
    
    Start time: Wed 2021-09-29, 15:21:39 (+0200)
    
    Simulation process uses 4 of 4 available OpenMP threads (system default).
    
    BLAS and LAPACK libraries use 4 of 4 available threads (system default).
    
    Preparing input validator...
    Reading input file (E:\nextnano Users\heorhii.yehiazarian\nextnanopy\nextnanopy_package\nextnanopy\docs\examples\input_files\sweep_example__ALLOY_0.3_SIZE_80_.in)...
    
    
    WARNING: Using database specified in command line.
    
    Preparing database validator...
    Reading database file (C:\Program Files\nextnano\2021_05_10\nextnano++\Syntax\database_nnp.in)...
    
    
    Material database initialized.
    
    Checking license:
    	 Valid From: 2021-5-3 To: 2022-12-31
    	 Licensed to: E-mail: heorhii.yehiazarian@nextnano.com-2022-12-31-nxt3
    
    ********* SETUP SIMULATION *****************************************************
    
    NOTE: Using output directory specified from command line (nextnanomat), 
    
    NOTE: Setting output directory to: E:\nextnano Users\heorhii.yehiazarian\nextnanopy\nextnanopy_output\sweep_example_sweep__ALLOY__SIZE9\sweep_example__ALLOY_0.3_SIZE_80_\
    
    ********* Simulation Grid *********
    
    Creating grid 1 using:
        pos = 0     	spacing = 0.5
        pos = 10     	spacing = 0.5
        pos = 20     	spacing = 0.5
        pos = 30     	spacing = 0.5
        pos = 90     	spacing = 0.1
        pos = 400     	spacing = 5
    
    Grid dimension: 548 * 1 * 1 
    Number of unique grid points: 548
    Range in 1-direction:   0 , ... , 400
    
    
    ********* Rotation Matrix *********
     1.0000000,  0.0000000,  0.0000000
     0.0000000,  1.0000000,  0.0000000
     0.0000000,  0.0000000,  1.0000000
    
    ********* Periodicity *************
      0-direction:  not periodic
    
    
    Start initializing structure.
    Finished initializing structure.
    Structure initialization time: 0[s]
    
    Setting reference vacuum level to 6.3 eV.
    
    NOTE: Electron minimum density is 1e+10 cm^-3.
    NOTE: Hole minimum density is 1e+10 cm^-3.
    
    NOTE: Electron maximum density is 1e+30 cm^-3.
    NOTE: Hole maximum density is 1e+30 cm^-3.
    
    NOTE: Minimal recombination is DISABLED.
    
    ***** Quantum Subgrid (2DEG) ******     
    Gridsize: 
    Grid dimension: 249 * 1 * 1 
    Number of unique grid points: 249
    Range in 1-direction:   85.0319539 , ... , 248.032375
    
    Calculating quantum density of states ... (2DEG_Gamma)
    
    ********* STRUCTURE OUTPUT *****************************************************
    Writing material indices...
    Writing contact indices...
    Writing donor density...
    Writing fixed charge density...
    
    ********* START CALCULATION ****************************************************
    
    Determine dirichlet points for contacts...
    Determine intrinsic density...
    Intrinsic density time: 0[s]
    
    Discretizing Poisson equation...
    
    
    
    
    ========= STARTING CALCULATION FOR BIAS POINT ==================================
    gate  0 V   backgate  -0 V   
    
    Determine electron Fermi level dirichlet values in contacts...
    Determine hole Fermi level dirichlet values in contacts...
    Initialize Fermi levels...
    Fermi level initialization time: 0[s]
    Initialize contacts as charge neutral...
    Determine potential Dirichlet values in Schottky and ohmic contacts...
    Update contact discretization in Poisson equation...
    
    Initialize electrostatic potential...
    Charge Neutrality time: 0.001[s]
    
    Solving nonlinear Poisson equation...
      Newton step: 1	89.06098129434528
      Newton step: 2	7.481685423405345
      Newton step: 3	1.43984460724948
      Newton step: 4	0.2775619229546668
      Newton step: 5	0.05442436986962094
      Newton step: 6	0.01203158025135868
      Newton step: 7	0.003954477372363758
      Newton step: 8	0.002006649927484391
      Newton step: 9	0.0001530601137750341
      Newton step: 10	4.972988069151158e-05
      Newton step: 11	1.47764200032421e-05
      Newton step: 12	2.813911753191068e-06
      Newton step: 13	1.465126144664157e-07
      Newton step: 14	4.335616759263277e-10
      Newton achieved/desired residual: 5.62296031e-13 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51800187
      conduction band minimum: -0.0278041201
    
     Solving 1 exact 1-band Schroedinger equation(s):
        Tridiagonal real symmetric eigenvalue solver:           1          10
    
    Computing densities...
    
    ******  SOLVING QUANTUM-POISSON EQUATIONS *----------------------------
    *----  Terminates after:   max_iter = 30
                            residual =       1.000000000e+05
    
    QUANTUM-POISSON:  iteration = 1 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	0.003564354209394014
      Newton step: 2	0.0006444409481518294
      Newton step: 3	1.274691075522498e-05
      Newton step: 4	5.11022945765301e-09
      Newton achieved/desired residual: 5.3679111e-13 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51791479
      conduction band minimum: -0.0384996935
    
     Solving 1 approximate (subspace) 1-band Schroedinger equation(s):
       Solving dense hermitian eigenvalue problem (standard solver)...
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 1.261862807e+11   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 1.070368955e-02
    
    QUANTUM-POISSON:  iteration = 2 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	0.0008901366968507922
      Newton step: 2	7.916418277605885e-06
      Newton step: 3	2.726405834812196e-08
      Newton achieved/desired residual: 8.02414716e-13 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51788994
      conduction band minimum: -0.0392992043
    
     Solving 1 exact 1-band Schroedinger equation(s):
        Tridiagonal real symmetric eigenvalue solver:           1          10
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 2.568348129e+10   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 7.995351599e-04
    
    QUANTUM-POISSON:  iteration = 3 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	0.0002802969751265204
      Newton step: 2	1.148098912283081e-06
      Newton achieved/desired residual: 5.68252327e-11 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51789207
      conduction band minimum: -0.0388850626
    
     Solving 1 approximate (subspace) 1-band Schroedinger equation(s):
       Solving dense hermitian eigenvalue problem (standard solver)...
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 5.877166312e+09   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 4.146481049e-04
    
    QUANTUM-POISSON:  iteration = 4 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	5.20829174163093e-05
      Newton step: 2	1.100092234916413e-08
      Newton achieved/desired residual: 5.64769141e-13 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51789137
      conduction band minimum: -0.0388561529
    
     Solving 1 exact 1-band Schroedinger equation(s):
        Tridiagonal real symmetric eigenvalue solver:           1          10
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 1.197851016e+09   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 3.103745759e-05
    
    QUANTUM-POISSON:  iteration = 5 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	1.199739308477293e-05
      Newton step: 2	4.211591175518618e-10
      Newton achieved/desired residual: 5.13566605e-13 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51789157
      conduction band minimum: -0.0388646175
    
     Solving 1 approximate (subspace) 1-band Schroedinger equation(s):
       Solving dense hermitian eigenvalue problem (standard solver)...
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 7.522643966e+07   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 8.464641819e-06
    
    QUANTUM-POISSON:  iteration = 6 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	2.159780684429558e-06
      Newton achieved/desired residual: 1.58758135e-11 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51789156
      conduction band minimum: -0.0388660521
    
     Solving 1 exact 1-band Schroedinger equation(s):
        Tridiagonal real symmetric eigenvalue solver:           1          10
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 4.844156467e+07   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 1.434902262e-06
    
    QUANTUM-POISSON:  iteration = 7 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	4.841511817166828e-07
      Newton achieved/desired residual: 9.15227995e-13 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51789155
      conduction band minimum: -0.0388656864
    
     Solving 1 approximate (subspace) 1-band Schroedinger equation(s):
       Solving dense hermitian eigenvalue problem (standard solver)...
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 3.253110323e+06   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 3.656993850e-07
    
    QUANTUM-POISSON:  iteration = 8 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	8.880328429256149e-08
      Newton achieved/desired residual: 5.4840886e-13 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51789155
      conduction band minimum: -0.0388656276
    
     Solving 1 exact 1-band Schroedinger equation(s):
        Tridiagonal real symmetric eigenvalue solver:           1          10
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 1.978814183e+06   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 5.880266318e-08
    
    QUANTUM-POISSON:  iteration = 9 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	1.954209869234108e-08
      Newton achieved/desired residual: 5.47778436e-13 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51789155
      conduction band minimum: -0.0388656425
    
     Solving 1 approximate (subspace) 1-band Schroedinger equation(s):
       Solving dense hermitian eigenvalue problem (standard solver)...
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 1.225408890e+05   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 1.489591428e-08
    
    QUANTUM-POISSON:  iteration = 10 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	3.606439662386792e-09
      Newton achieved/desired residual: 5.76464128e-13 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51789155
      conduction band minimum: -0.0388656449
    
     Solving 1 exact 1-band Schroedinger equation(s):
        Tridiagonal real symmetric eigenvalue solver:           1          10
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 7.945905520e+04   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 2.426816081e-09
    
    *----  SOLVING QUANTUM-POISSON FINISHED ----------------------------
    
    Solving Quantum Mechanics ---- (quantum regions without density only)
    
    
    Solving Quantum Mechanics ---- (determine k-dispersion only)
    
    
    ********* OUTPUT ***************************************************************
    
    Writing characteristics data(1)...
    Writing characteristics data(2)...
    
    Writing electrostatic potential...
    
    Writing band edges...
    
    Writing Fermi levels...
    
    Writing results from quantum calculations...
    
    Writing carrier densities...
    Writing ionized dopant densities...
    
    ********* FINISHED CALCULATION *************************************************
    
    End time: Wed 2021-09-29, 15:21:40 (+0200)
    Total Poisson Solver Time: 0.014[s]
    Total Quantum Solver Time: 0.006[s]
    Simulator Run Time: 0.59[s]
    
    ================================================================================
    DONE.
    ================================================================================
    ================================================================================
    STARTING...
    ================================================================================
    Starting execution as:
    C:\Program Files\nextnano\2021_05_10\nextnano++\bin 64bit\nextnano++_Intel_64bit.exe --license C:\Users\heorhii.yehiazarian\Documents\nextnano\License\License_nnp.lic --database C:\Program Files\nextnano\2021_05_10\nextnano++\Syntax\database_nnp.in --threads 0 --outputdirectory E:\nextnano Users\heorhii.yehiazarian\nextnanopy\nextnanopy_output\sweep_example_sweep__ALLOY__SIZE9\sweep_example__ALLOY_0.3_SIZE_100_ --noautooutdir E:\nextnano Users\heorhii.yehiazarian\nextnanopy\nextnanopy_package\nextnanopy\docs\examples\input_files\sweep_example__ALLOY_0.3_SIZE_100_.in 
    
    nextnano++ (1.7.54 - 2021.050601) May 10 2021
    =============================================================================
    COPYRIGHT NOTICE                                                             
    =============================================================================
    Please read the file 'copyright_nextnano++.txt' in your installation folder  
    for further information about the terms of copyright of the nextnano++ code  
    and of third party source codes and libraries used in the nextnano++ code.   
                                                                                 
    In case this file is missing or seems incomplete or corrupted, please contact
    nextnano GmbH, Germany by submitting a support request on www.nextnano.de or 
    by sending an email to support@nextnano.com in order to receive a new copy.  
                                                                                 
    ANY USE OF THE NEXTNANO++ CODE CONSTITUTES ACCEPTANCE OF THE TERMS OF THE    
    COPYRIGHT NOTICE.                                                            
    =============================================================================
    
    
    =============================================================================
     PROCESSING FILE: E:\nextnano Users\heorhii.yehiazarian\nextnanopy\nextnanopy_package\nextnanopy\docs\examples\input_files\sweep_example__ALLOY_0.3_SIZE_100_.in
    =============================================================================
    
    Start time: Wed 2021-09-29, 15:21:40 (+0200)
    
    Simulation process uses 4 of 4 available OpenMP threads (system default).
    
    BLAS and LAPACK libraries use 4 of 4 available threads (system default).
    
    Preparing input validator...
    Reading input file (E:\nextnano Users\heorhii.yehiazarian\nextnanopy\nextnanopy_package\nextnanopy\docs\examples\input_files\sweep_example__ALLOY_0.3_SIZE_100_.in)...
    
    
    WARNING: Using database specified in command line.
    
    Preparing database validator...
    Reading database file (C:\Program Files\nextnano\2021_05_10\nextnano++\Syntax\database_nnp.in)...
    
    
    Material database initialized.
    
    Checking license:
    	 Valid From: 2021-5-3 To: 2022-12-31
    	 Licensed to: E-mail: heorhii.yehiazarian@nextnano.com-2022-12-31-nxt3
    
    ********* SETUP SIMULATION *****************************************************
    
    NOTE: Using output directory specified from command line (nextnanomat), 
    
    NOTE: Setting output directory to: E:\nextnano Users\heorhii.yehiazarian\nextnanopy\nextnanopy_output\sweep_example_sweep__ALLOY__SIZE9\sweep_example__ALLOY_0.3_SIZE_100_\
    
    ********* Simulation Grid *********
    
    Creating grid 1 using:
        pos = 0     	spacing = 0.5
        pos = 10     	spacing = 0.5
        pos = 40     	spacing = 0.5
        pos = 50     	spacing = 0.5
        pos = 110     	spacing = 0.1
        pos = 400     	spacing = 5
    
    Grid dimension: 572 * 1 * 1 
    Number of unique grid points: 572
    Range in 1-direction:   0 , ... , 400
    
    
    ********* Rotation Matrix *********
     1.0000000,  0.0000000,  0.0000000
     0.0000000,  1.0000000,  0.0000000
     0.0000000,  0.0000000,  1.0000000
    
    ********* Periodicity *************
      0-direction:  not periodic
    
    
    Start initializing structure.
    Finished initializing structure.
    Structure initialization time: 0[s]
    
    Setting reference vacuum level to 6.3 eV.
    
    NOTE: Electron minimum density is 1e+10 cm^-3.
    NOTE: Hole minimum density is 1e+10 cm^-3.
    
    NOTE: Electron maximum density is 1e+30 cm^-3.
    NOTE: Hole maximum density is 1e+30 cm^-3.
    
    NOTE: Minimal recombination is DISABLED.
    
    ***** Quantum Subgrid (2DEG) ******     
    Gridsize: 
    Grid dimension: 232 * 1 * 1 
    Number of unique grid points: 232
    Range in 1-direction:   105.031954 , ... , 248.470823
    
    Calculating quantum density of states ... (2DEG_Gamma)
    
    ********* STRUCTURE OUTPUT *****************************************************
    Writing material indices...
    Writing contact indices...
    Writing donor density...
    Writing fixed charge density...
    
    ********* START CALCULATION ****************************************************
    
    Determine dirichlet points for contacts...
    Determine intrinsic density...
    Intrinsic density time: 0.001[s]
    
    Discretizing Poisson equation...
    
    
    
    
    ========= STARTING CALCULATION FOR BIAS POINT ==================================
    gate  0 V   backgate  -0 V   
    
    Determine electron Fermi level dirichlet values in contacts...
    Determine hole Fermi level dirichlet values in contacts...
    Initialize Fermi levels...
    Fermi level initialization time: 0[s]
    Initialize contacts as charge neutral...
    Determine potential Dirichlet values in Schottky and ohmic contacts...
    Update contact discretization in Poisson equation...
    
    Initialize electrostatic potential...
    Charge Neutrality time: 0.002[s]
    
    Solving nonlinear Poisson equation...
      Newton step: 1	89.06098127827575
      Newton step: 2	7.522535360551922
      Newton step: 3	1.447593939134491
      Newton step: 4	0.2790849288507246
      Newton step: 5	0.05480875689534115
      Newton step: 6	0.01205081051847407
      Newton step: 7	0.002932256202112084
      Newton step: 8	0.00051728477543731
      Newton step: 9	0.0001506119368545961
      Newton step: 10	4.835160544028204e-05
      Newton step: 11	1.386145508916643e-05
      Newton step: 12	2.348683818826961e-06
      Newton step: 13	9.222756242137165e-08
      Newton achieved/desired residual: 1.52172729e-10 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51812355
      conduction band minimum: -0.0321466401
    
     Solving 1 exact 1-band Schroedinger equation(s):
        Tridiagonal real symmetric eigenvalue solver:           1          10
    
    Computing densities...
    
    ******  SOLVING QUANTUM-POISSON EQUATIONS *----------------------------
    *----  Terminates after:   max_iter = 30
                            residual =       1.000000000e+05
    
    QUANTUM-POISSON:  iteration = 1 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	0.004240099791106252
      Newton step: 2	0.0006441248078269212
      Newton step: 3	1.07311692889481e-05
      Newton step: 4	2.833234961383025e-09
      Newton achieved/desired residual: 5.20260785e-13 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51801942
      conduction band minimum: -0.0433059257
    
     Solving 1 approximate (subspace) 1-band Schroedinger equation(s):
       Solving dense hermitian eigenvalue problem (standard solver)...
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 1.511874581e+11   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 1.117793175e-02
    
    QUANTUM-POISSON:  iteration = 2 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	0.0009311261000731731
      Newton step: 2	5.754072409028792e-06
      Newton step: 3	8.15081053563486e-09
      Newton achieved/desired residual: 5.88199485e-13 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51798359
      conduction band minimum: -0.0439746563
    
     Solving 1 exact 1-band Schroedinger equation(s):
        Tridiagonal real symmetric eigenvalue solver:           1          10
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 2.343675239e+10   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 6.688471280e-04
    
    QUANTUM-POISSON:  iteration = 3 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	0.000246434997954156
      Newton step: 2	6.367500835452753e-07
      Newton achieved/desired residual: 2.14708252e-11 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51798179
      conduction band minimum: -0.0436612821
    
     Solving 1 approximate (subspace) 1-band Schroedinger equation(s):
       Solving dense hermitian eigenvalue problem (standard solver)...
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 4.677322350e+09   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 3.139362349e-04
    
    QUANTUM-POISSON:  iteration = 4 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	4.35327854532424e-05
      Newton step: 2	4.861666625817756e-09
      Newton achieved/desired residual: 6.16691884e-13 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51798146
      conduction band minimum: -0.0436395332
    
     Solving 1 exact 1-band Schroedinger equation(s):
        Tridiagonal real symmetric eigenvalue solver:           1          10
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 8.936740627e+08   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 2.314062349e-05
    
    QUANTUM-POISSON:  iteration = 5 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	8.753261432458775e-06
      Newton achieved/desired residual: 1.71391104e-10 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51798152
      conduction band minimum: -0.043644913
    
     Solving 1 approximate (subspace) 1-band Schroedinger equation(s):
       Solving dense hermitian eigenvalue problem (standard solver)...
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 4.995265069e+07   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 5.379780065e-06
    
    QUANTUM-POISSON:  iteration = 6 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	1.441922380284213e-06
      Newton achieved/desired residual: 7.67490673e-12 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51798149
      conduction band minimum: -0.0436457794
    
     Solving 1 exact 1-band Schroedinger equation(s):
        Tridiagonal real symmetric eigenvalue solver:           1          10
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 2.949673903e+07   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 8.669680285e-07
    
    QUANTUM-POISSON:  iteration = 7 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	2.920443448700613e-07
      Newton achieved/desired residual: 6.95841612e-13 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51798148
      conduction band minimum: -0.0436455995
    
     Solving 1 approximate (subspace) 1-band Schroedinger equation(s):
       Solving dense hermitian eigenvalue problem (standard solver)...
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 2.020868316e+06   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 1.798615155e-07
    
    QUANTUM-POISSON:  iteration = 8 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	4.850389054665009e-08
      Newton achieved/desired residual: 5.27080167e-13 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51798148
      conduction band minimum: -0.0436455721
    
     Solving 1 exact 1-band Schroedinger equation(s):
        Tridiagonal real symmetric eigenvalue solver:           1          10
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 9.989825197e+05   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 2.740622884e-08
    
    QUANTUM-POISSON:  iteration = 9 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	9.601859380294538e-09
      Newton achieved/desired residual: 5.8511211e-13 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51798148
      conduction band minimum: -0.0436455784
    
     Solving 1 approximate (subspace) 1-band Schroedinger equation(s):
       Solving dense hermitian eigenvalue problem (standard solver)...
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 5.551384445e+04   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 6.281562381e-09
    
    QUANTUM-POISSON:  iteration = 10 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	1.636386360606356e-09
      Newton achieved/desired residual: 5.60487328e-13 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51798148
      conduction band minimum: -0.0436455794
    
     Solving 1 exact 1-band Schroedinger equation(s):
        Tridiagonal real symmetric eigenvalue solver:           1          10
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 3.371463284e+04   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 1.007739225e-09
    
    *----  SOLVING QUANTUM-POISSON FINISHED ----------------------------
    
    Solving Quantum Mechanics ---- (quantum regions without density only)
    
    
    Solving Quantum Mechanics ---- (determine k-dispersion only)
    
    
    ********* OUTPUT ***************************************************************
    
    Writing characteristics data(1)...
    Writing characteristics data(2)...
    
    Writing electrostatic potential...
    
    Writing band edges...
    
    Writing Fermi levels...
    
    Writing results from quantum calculations...
    
    Writing carrier densities...
    Writing ionized dopant densities...
    
    ********* FINISHED CALCULATION *************************************************
    
    End time: Wed 2021-09-29, 15:21:41 (+0200)
    Total Poisson Solver Time: 0.009[s]
    Total Quantum Solver Time: 0.009[s]
    Simulator Run Time: 0.589[s]
    
    ================================================================================
    DONE.
    ================================================================================
    ================================================================================
    STARTING...
    ================================================================================
    Starting execution as:
    C:\Program Files\nextnano\2021_05_10\nextnano++\bin 64bit\nextnano++_Intel_64bit.exe --license C:\Users\heorhii.yehiazarian\Documents\nextnano\License\License_nnp.lic --database C:\Program Files\nextnano\2021_05_10\nextnano++\Syntax\database_nnp.in --threads 0 --outputdirectory E:\nextnano Users\heorhii.yehiazarian\nextnanopy\nextnanopy_output\sweep_example_sweep__ALLOY__SIZE9\sweep_example__ALLOY_0.6_SIZE_80_ --noautooutdir E:\nextnano Users\heorhii.yehiazarian\nextnanopy\nextnanopy_package\nextnanopy\docs\examples\input_files\sweep_example__ALLOY_0.6_SIZE_80_.in 
    
    nextnano++ (1.7.54 - 2021.050601) May 10 2021
    =============================================================================
    COPYRIGHT NOTICE                                                             
    =============================================================================
    Please read the file 'copyright_nextnano++.txt' in your installation folder  
    for further information about the terms of copyright of the nextnano++ code  
    and of third party source codes and libraries used in the nextnano++ code.   
                                                                                 
    In case this file is missing or seems incomplete or corrupted, please contact
    nextnano GmbH, Germany by submitting a support request on www.nextnano.de or 
    by sending an email to support@nextnano.com in order to receive a new copy.  
                                                                                 
    ANY USE OF THE NEXTNANO++ CODE CONSTITUTES ACCEPTANCE OF THE TERMS OF THE    
    COPYRIGHT NOTICE.                                                            
    =============================================================================
    
    
    =============================================================================
     PROCESSING FILE: E:\nextnano Users\heorhii.yehiazarian\nextnanopy\nextnanopy_package\nextnanopy\docs\examples\input_files\sweep_example__ALLOY_0.6_SIZE_80_.in
    =============================================================================
    
    Start time: Wed 2021-09-29, 15:21:41 (+0200)
    
    Simulation process uses 4 of 4 available OpenMP threads (system default).
    
    BLAS and LAPACK libraries use 4 of 4 available threads (system default).
    
    Preparing input validator...
    Reading input file (E:\nextnano Users\heorhii.yehiazarian\nextnanopy\nextnanopy_package\nextnanopy\docs\examples\input_files\sweep_example__ALLOY_0.6_SIZE_80_.in)...
    
    
    WARNING: Using database specified in command line.
    
    Preparing database validator...
    Reading database file (C:\Program Files\nextnano\2021_05_10\nextnano++\Syntax\database_nnp.in)...
    
    
    Material database initialized.
    
    Checking license:
    	 Valid From: 2021-5-3 To: 2022-12-31
    	 Licensed to: E-mail: heorhii.yehiazarian@nextnano.com-2022-12-31-nxt3
    
    ********* SETUP SIMULATION *****************************************************
    
    NOTE: Using output directory specified from command line (nextnanomat), 
    
    NOTE: Setting output directory to: E:\nextnano Users\heorhii.yehiazarian\nextnanopy\nextnanopy_output\sweep_example_sweep__ALLOY__SIZE9\sweep_example__ALLOY_0.6_SIZE_80_\
    
    ********* Simulation Grid *********
    
    Creating grid 1 using:
        pos = 0     	spacing = 0.5
        pos = 10     	spacing = 0.5
        pos = 20     	spacing = 0.5
        pos = 30     	spacing = 0.5
        pos = 90     	spacing = 0.1
        pos = 400     	spacing = 5
    
    Grid dimension: 548 * 1 * 1 
    Number of unique grid points: 548
    Range in 1-direction:   0 , ... , 400
    
    
    ********* Rotation Matrix *********
     1.0000000,  0.0000000,  0.0000000
     0.0000000,  1.0000000,  0.0000000
     0.0000000,  0.0000000,  1.0000000
    
    ********* Periodicity *************
      0-direction:  not periodic
    
    
    Start initializing structure.
    Finished initializing structure.
    Structure initialization time: 0[s]
    
    Setting reference vacuum level to 6.3 eV.
    
    NOTE: Electron minimum density is 1e+10 cm^-3.
    NOTE: Hole minimum density is 1e+10 cm^-3.
    
    NOTE: Electron maximum density is 1e+30 cm^-3.
    NOTE: Hole maximum density is 1e+30 cm^-3.
    
    NOTE: Minimal recombination is DISABLED.
    
    ***** Quantum Subgrid (2DEG) ******     
    Gridsize: 
    Grid dimension: 249 * 1 * 1 
    Number of unique grid points: 249
    Range in 1-direction:   85.0319539 , ... , 248.032375
    
    Calculating quantum density of states ... (2DEG_Gamma)
    
    ********* STRUCTURE OUTPUT *****************************************************
    Writing material indices...
    Writing contact indices...
    Writing donor density...
    Writing fixed charge density...
    
    ********* START CALCULATION ****************************************************
    
    Determine dirichlet points for contacts...
    Determine intrinsic density...
    Intrinsic density time: 0.001[s]
    
    Discretizing Poisson equation...
    
    
    
    
    ========= STARTING CALCULATION FOR BIAS POINT ==================================
    gate  0 V   backgate  -0 V   
    
    Determine electron Fermi level dirichlet values in contacts...
    Determine hole Fermi level dirichlet values in contacts...
    Initialize Fermi levels...
    Fermi level initialization time: 0[s]
    Initialize contacts as charge neutral...
    Determine potential Dirichlet values in Schottky and ohmic contacts...
    Update contact discretization in Poisson equation...
    
    Initialize electrostatic potential...
    Charge Neutrality time: 0.002[s]
    
    Solving nonlinear Poisson equation...
      Newton step: 1	107.2490244863562
      Newton step: 2	15.66898519579072
      Newton step: 3	3.015744008774924
      Newton step: 4	0.5812959491250699
      Newton step: 5	0.1137413076834727
      Newton step: 6	0.02198460870624287
      Newton step: 7	0.004179282344877126
      Newton step: 8	0.0009064315880132435
      Newton step: 9	0.0002560904358707241
      Newton step: 10	8.23137138503286e-05
      Newton step: 11	2.60653826530117e-05
      Newton step: 12	6.493224577154813e-06
      Newton step: 13	6.945332616544747e-07
      Newton step: 14	9.521991352969682e-09
      Newton achieved/desired residual: 1.91103121e-12 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51800451
      conduction band minimum: -0.0295473461
    
     Solving 1 exact 1-band Schroedinger equation(s):
        Tridiagonal real symmetric eigenvalue solver:           1          10
    
    Computing densities...
    
    ******  SOLVING QUANTUM-POISSON EQUATIONS *----------------------------
    *----  Terminates after:   max_iter = 30
                            residual =       1.000000000e+05
    
    QUANTUM-POISSON:  iteration = 1 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	0.003930441495130048
      Newton step: 2	0.000786133641277543
      Newton step: 3	1.656338290292209e-05
      Newton step: 4	7.267234531034789e-09
      Newton achieved/desired residual: 5.59120803e-13 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51791885
      conduction band minimum: -0.0416644706
    
     Solving 1 approximate (subspace) 1-band Schroedinger equation(s):
       Solving dense hermitian eigenvalue problem (standard solver)...
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 1.400690630e+11   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 1.212231928e-02
    
    QUANTUM-POISSON:  iteration = 2 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	0.001016019186684537
      Newton step: 2	8.344822981379541e-06
      Newton step: 3	2.332364442089842e-08
      Newton achieved/desired residual: 6.00673247e-13 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51788599
      conduction band minimum: -0.0426052645
    
     Solving 1 exact 1-band Schroedinger equation(s):
        Tridiagonal real symmetric eigenvalue solver:           1          10
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 3.093900463e+10   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 9.415952884e-04
    
    QUANTUM-POISSON:  iteration = 3 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	0.0003617081293552383
      Newton step: 2	1.870394896498522e-06
      Newton achieved/desired residual: 1.39086748e-10 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51789061
      conduction band minimum: -0.0420875977
    
     Solving 1 approximate (subspace) 1-band Schroedinger equation(s):
       Solving dense hermitian eigenvalue problem (standard solver)...
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 7.589730041e+09   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 5.192834047e-04
    
    QUANTUM-POISSON:  iteration = 4 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	6.505484046818111e-05
      Newton step: 2	1.405929064315233e-08
      Newton achieved/desired residual: 5.17169737e-13 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51788995
      conduction band minimum: -0.0420528321
    
     Solving 1 exact 1-band Schroedinger equation(s):
        Tridiagonal real symmetric eigenvalue solver:           1          10
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 1.571671836e+09   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 3.826031298e-05
    
    QUANTUM-POISSON:  iteration = 5 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	1.693668612463233e-05
      Newton step: 2	8.584067074657285e-10
      Newton achieved/desired residual: 5.26503923e-13 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51789018
      conduction band minimum: -0.0420645632
    
     Solving 1 approximate (subspace) 1-band Schroedinger equation(s):
       Solving dense hermitian eigenvalue problem (standard solver)...
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 1.085744003e+08   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 1.174340340e-05
    
    QUANTUM-POISSON:  iteration = 6 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	3.039852571582908e-06
      Newton achieved/desired residual: 3.04553416e-11 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51789017
      conduction band minimum: -0.0420665019
    
     Solving 1 exact 1-band Schroedinger equation(s):
        Tridiagonal real symmetric eigenvalue solver:           1          10
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 7.094372303e+07   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 1.941553613e-06
    
    QUANTUM-POISSON:  iteration = 7 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	7.558168459344952e-07
      Newton achieved/desired residual: 1.95735754e-12 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51789016
      conduction band minimum: -0.0420659406
    
     Solving 1 approximate (subspace) 1-band Schroedinger equation(s):
       Solving dense hermitian eigenvalue problem (standard solver)...
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 5.274009510e+06   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 5.619444132e-07
    
    QUANTUM-POISSON:  iteration = 8 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	1.381003941897698e-07
      Newton achieved/desired residual: 5.2299086e-13 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51789016
      conduction band minimum: -0.0420658527
    
     Solving 1 exact 1-band Schroedinger equation(s):
        Tridiagonal real symmetric eigenvalue solver:           1          10
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 3.203367324e+06   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 8.798308748e-08
    
    QUANTUM-POISSON:  iteration = 9 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	3.376206365005711e-08
      Newton achieved/desired residual: 5.26060184e-13 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51789016
      conduction band minimum: -0.042065878
    
     Solving 1 approximate (subspace) 1-band Schroedinger equation(s):
       Solving dense hermitian eigenvalue problem (standard solver)...
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 2.194783687e+05   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 2.528681931e-08
    
    QUANTUM-POISSON:  iteration = 10 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	6.206865670418685e-09
      Newton achieved/desired residual: 5.3161354e-13 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51789016
      conduction band minimum: -0.042065882
    
     Solving 1 exact 1-band Schroedinger equation(s):
        Tridiagonal real symmetric eigenvalue solver:           1          10
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 1.421174353e+05   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 4.016427635e-09
    
    QUANTUM-POISSON:  iteration = 11 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	1.511907924383729e-09
      Newton achieved/desired residual: 5.39567809e-13 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51789016
      conduction band minimum: -0.0420658809
    
     Solving 1 approximate (subspace) 1-band Schroedinger equation(s):
       Solving dense hermitian eigenvalue problem (standard solver)...
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 1.045240092e+04   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 1.125005866e-09
    
    QUANTUM-POISSON:  iteration = 12 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	2.773354334312728e-10
      Newton achieved/desired residual: 5.2356044e-13 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51789016
      conduction band minimum: -0.0420658807
    
     Solving 1 exact 1-band Schroedinger equation(s):
        Tridiagonal real symmetric eigenvalue solver:           1          10
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 6.425305994e+03   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 1.773758918e-10
    
    *----  SOLVING QUANTUM-POISSON FINISHED ----------------------------
    
    Solving Quantum Mechanics ---- (quantum regions without density only)
    
    
    Solving Quantum Mechanics ---- (determine k-dispersion only)
    
    
    ********* OUTPUT ***************************************************************
    
    Writing characteristics data(1)...
    Writing characteristics data(2)...
    
    Writing electrostatic potential...
    
    Writing band edges...
    
    Writing Fermi levels...
    
    Writing results from quantum calculations...
    
    Writing carrier densities...
    Writing ionized dopant densities...
    
    ********* FINISHED CALCULATION *************************************************
    
    End time: Wed 2021-09-29, 15:21:41 (+0200)
    Total Poisson Solver Time: 0.011[s]
    Total Quantum Solver Time: 0.009[s]
    Simulator Run Time: 0.601[s]
    
    ================================================================================
    DONE.
    ================================================================================
    ================================================================================
    STARTING...
    ================================================================================
    Starting execution as:
    C:\Program Files\nextnano\2021_05_10\nextnano++\bin 64bit\nextnano++_Intel_64bit.exe --license C:\Users\heorhii.yehiazarian\Documents\nextnano\License\License_nnp.lic --database C:\Program Files\nextnano\2021_05_10\nextnano++\Syntax\database_nnp.in --threads 0 --outputdirectory E:\nextnano Users\heorhii.yehiazarian\nextnanopy\nextnanopy_output\sweep_example_sweep__ALLOY__SIZE9\sweep_example__ALLOY_0.6_SIZE_100_ --noautooutdir E:\nextnano Users\heorhii.yehiazarian\nextnanopy\nextnanopy_package\nextnanopy\docs\examples\input_files\sweep_example__ALLOY_0.6_SIZE_100_.in 
    
    nextnano++ (1.7.54 - 2021.050601) May 10 2021
    =============================================================================
    COPYRIGHT NOTICE                                                             
    =============================================================================
    Please read the file 'copyright_nextnano++.txt' in your installation folder  
    for further information about the terms of copyright of the nextnano++ code  
    and of third party source codes and libraries used in the nextnano++ code.   
                                                                                 
    In case this file is missing or seems incomplete or corrupted, please contact
    nextnano GmbH, Germany by submitting a support request on www.nextnano.de or 
    by sending an email to support@nextnano.com in order to receive a new copy.  
                                                                                 
    ANY USE OF THE NEXTNANO++ CODE CONSTITUTES ACCEPTANCE OF THE TERMS OF THE    
    COPYRIGHT NOTICE.                                                            
    =============================================================================
    
    
    =============================================================================
     PROCESSING FILE: E:\nextnano Users\heorhii.yehiazarian\nextnanopy\nextnanopy_package\nextnanopy\docs\examples\input_files\sweep_example__ALLOY_0.6_SIZE_100_.in
    =============================================================================
    
    Start time: Wed 2021-09-29, 15:21:41 (+0200)
    
    Simulation process uses 4 of 4 available OpenMP threads (system default).
    
    BLAS and LAPACK libraries use 4 of 4 available threads (system default).
    
    Preparing input validator...
    Reading input file (E:\nextnano Users\heorhii.yehiazarian\nextnanopy\nextnanopy_package\nextnanopy\docs\examples\input_files\sweep_example__ALLOY_0.6_SIZE_100_.in)...
    
    
    WARNING: Using database specified in command line.
    
    Preparing database validator...
    Reading database file (C:\Program Files\nextnano\2021_05_10\nextnano++\Syntax\database_nnp.in)...
    
    
    Material database initialized.
    
    Checking license:
    	 Valid From: 2021-5-3 To: 2022-12-31
    	 Licensed to: E-mail: heorhii.yehiazarian@nextnano.com-2022-12-31-nxt3
    
    ********* SETUP SIMULATION *****************************************************
    
    NOTE: Using output directory specified from command line (nextnanomat), 
    
    NOTE: Setting output directory to: E:\nextnano Users\heorhii.yehiazarian\nextnanopy\nextnanopy_output\sweep_example_sweep__ALLOY__SIZE9\sweep_example__ALLOY_0.6_SIZE_100_\
    
    ********* Simulation Grid *********
    
    Creating grid 1 using:
        pos = 0     	spacing = 0.5
        pos = 10     	spacing = 0.5
        pos = 40     	spacing = 0.5
        pos = 50     	spacing = 0.5
        pos = 110     	spacing = 0.1
        pos = 400     	spacing = 5
    
    Grid dimension: 572 * 1 * 1 
    Number of unique grid points: 572
    Range in 1-direction:   0 , ... , 400
    
    
    ********* Rotation Matrix *********
     1.0000000,  0.0000000,  0.0000000
     0.0000000,  1.0000000,  0.0000000
     0.0000000,  0.0000000,  1.0000000
    
    ********* Periodicity *************
      0-direction:  not periodic
    
    
    Start initializing structure.
    Finished initializing structure.
    Structure initialization time: 0.001[s]
    
    Setting reference vacuum level to 6.3 eV.
    
    NOTE: Electron minimum density is 1e+10 cm^-3.
    NOTE: Hole minimum density is 1e+10 cm^-3.
    
    NOTE: Electron maximum density is 1e+30 cm^-3.
    NOTE: Hole maximum density is 1e+30 cm^-3.
    
    NOTE: Minimal recombination is DISABLED.
    
    ***** Quantum Subgrid (2DEG) ******     
    Gridsize: 
    Grid dimension: 232 * 1 * 1 
    Number of unique grid points: 232
    Range in 1-direction:   105.031954 , ... , 248.470823
    
    Calculating quantum density of states ... (2DEG_Gamma)
    
    ********* STRUCTURE OUTPUT *****************************************************
    Writing material indices...
    Writing contact indices...
    Writing donor density...
    Writing fixed charge density...
    
    ********* START CALCULATION ****************************************************
    
    Determine dirichlet points for contacts...
    Determine intrinsic density...
    Intrinsic density time: 0.001[s]
    
    Discretizing Poisson equation...
    
    
    
    
    ========= STARTING CALCULATION FOR BIAS POINT ==================================
    gate  0 V   backgate  -0 V   
    
    Determine electron Fermi level dirichlet values in contacts...
    Determine hole Fermi level dirichlet values in contacts...
    Initialize Fermi levels...
    Fermi level initialization time: 0.001[s]
    Initialize contacts as charge neutral...
    Determine potential Dirichlet values in Schottky and ohmic contacts...
    Update contact discretization in Poisson equation...
    
    Initialize electrostatic potential...
    Charge Neutrality time: 0.001[s]
    
    Solving nonlinear Poisson equation...
      Newton step: 1	107.2490244730118
      Newton step: 2	15.40064050442937
      Newton step: 3	2.963936660323407
      Newton step: 4	0.5713126831443344
      Newton step: 5	0.1118512070992721
      Newton step: 6	0.02478324515263767
      Newton step: 7	0.007453442902735021
      Newton step: 8	0.001212940092163133
      Newton step: 9	0.000248465817424785
      Newton step: 10	7.898274232465762e-05
      Newton step: 11	2.436482377490808e-05
      Newton step: 12	5.545972899553904e-06
      Newton step: 13	4.631459574536696e-07
      Newton step: 14	3.718155221821895e-09
      Newton achieved/desired residual: 5.49265177e-13 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51814269
      conduction band minimum: -0.0471080685
    
     Solving 1 exact 1-band Schroedinger equation(s):
        Tridiagonal real symmetric eigenvalue solver:           1          10
    
    Computing densities...
    
    ******  SOLVING QUANTUM-POISSON EQUATIONS *----------------------------
    *----  Terminates after:   max_iter = 30
                            residual =       1.000000000e+05
    
    QUANTUM-POISSON:  iteration = 1 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	0.006780907962587542
      Newton step: 2	0.0008450573151101406
      Newton step: 3	1.095595185118058e-05
      Newton step: 4	1.198650075012817e-09
      Newton achieved/desired residual: 5.06683755e-13 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51800732
      conduction band minimum: -0.0624994512
    
     Solving 1 approximate (subspace) 1-band Schroedinger equation(s):
       Solving dense hermitian eigenvalue problem (standard solver)...
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 2.176547461e+11   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 1.540090291e-02
    
    QUANTUM-POISSON:  iteration = 2 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	0.001457501059474673
      Newton step: 2	2.213351027098723e-06
      Newton step: 3	3.241551627174941e-09
      Newton achieved/desired residual: 5.15863358e-13 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51795284
      conduction band minimum: -0.0636178678
    
     Solving 1 exact 1-band Schroedinger equation(s):
        Tridiagonal real symmetric eigenvalue solver:           1          10
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 4.922540735e+10   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 1.118708177e-03
    
    QUANTUM-POISSON:  iteration = 3 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	0.0006792222491626357
      Newton step: 2	1.407859697888881e-06
      Newton achieved/desired residual: 4.45788112e-11 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51797237
      conduction band minimum: -0.0628987852
    
     Solving 1 approximate (subspace) 1-band Schroedinger equation(s):
       Solving dense hermitian eigenvalue problem (standard solver)...
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 1.162119041e+10   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 7.204824905e-04
    
    QUANTUM-POISSON:  iteration = 4 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	0.000106027388831513
      Newton step: 2	4.815429158710036e-09
      Newton achieved/desired residual: 5.38896678e-13 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51797286
      conduction band minimum: -0.0628478266
    
     Solving 1 exact 1-band Schroedinger equation(s):
        Tridiagonal real symmetric eigenvalue solver:           1          10
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 3.067753018e+09   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 5.278196966e-05
    
    QUANTUM-POISSON:  iteration = 5 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	4.176986639763025e-05
      Newton step: 2	1.26021595156157e-09
      Newton achieved/desired residual: 5.08913685e-13 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51797305
      conduction band minimum: -0.062873078
    
     Solving 1 approximate (subspace) 1-band Schroedinger equation(s):
       Solving dense hermitian eigenvalue problem (standard solver)...
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 3.002398516e+08   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 2.526379566e-05
    
    QUANTUM-POISSON:  iteration = 6 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	6.692281270876565e-06
      Newton achieved/desired residual: 2.31874211e-11 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51797306
      conduction band minimum: -0.0628764079
    
     Solving 1 exact 1-band Schroedinger equation(s):
        Tridiagonal real symmetric eigenvalue solver:           1          10
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 1.804775154e+08   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 3.331354431e-06
    
    QUANTUM-POISSON:  iteration = 7 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	2.416659463225632e-06
      Newton achieved/desired residual: 4.29719779e-12 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51797305
      conduction band minimum: -0.0628748897
    
     Solving 1 approximate (subspace) 1-band Schroedinger equation(s):
       Solving dense hermitian eigenvalue problem (standard solver)...
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 1.785389249e+07   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 1.518850970e-06
    
    QUANTUM-POISSON:  iteration = 8 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	3.899640363959461e-07
      Newton achieved/desired residual: 4.69415402e-13 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51797305
      conduction band minimum: -0.0628746943
    
     Solving 1 exact 1-band Schroedinger equation(s):
        Tridiagonal real symmetric eigenvalue solver:           1          10
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 1.056006115e+07   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 1.954524915e-07
    
    QUANTUM-POISSON:  iteration = 9 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	1.405256529744093e-07
      Newton achieved/desired residual: 4.86078114e-13 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51797306
      conduction band minimum: -0.0628747829
    
     Solving 1 approximate (subspace) 1-band Schroedinger equation(s):
       Solving dense hermitian eigenvalue problem (standard solver)...
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 9.883354682e+05   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 8.864090439e-08
    
    QUANTUM-POISSON:  iteration = 10 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	2.283215984250831e-08
      Newton achieved/desired residual: 5.23898358e-13 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51797306
      conduction band minimum: -0.0628747944
    
     Solving 1 exact 1-band Schroedinger equation(s):
        Tridiagonal real symmetric eigenvalue solver:           1          10
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 6.088371940e+05   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 1.154800966e-08
    
    QUANTUM-POISSON:  iteration = 11 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	8.14060118730117e-09
      Newton achieved/desired residual: 4.88434306e-13 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51797306
      conduction band minimum: -0.0628747893
    
     Solving 1 approximate (subspace) 1-band Schroedinger equation(s):
       Solving dense hermitian eigenvalue problem (standard solver)...
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 5.874909227e+04   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 5.121671087e-09
    
    QUANTUM-POISSON:  iteration = 12 of 30 ----------------------------
    
    Solving nonlinear Poisson equation...
      Newton step: 1	1.319775438979392e-09
      Newton achieved/desired residual: 5.07359365e-13 1.80951265e-10
    
    Solving Quantum Mechanics ---- (and calculate density)
    
      valence band maximum: -1.51797306
      conduction band minimum: -0.0628747887
    
     Solving 1 exact 1-band Schroedinger equation(s):
        Tridiagonal real symmetric eigenvalue solver:           1          10
    
    Computing densities...
    
    QUANTUM-POISSON:   Residual_EDensity = 3.551998432e+04   Residual_HDensity = 0.000000000e+00
    QUANTUM-POISSON:   Residual_potential = 6.653881890e-10
    
    *----  SOLVING QUANTUM-POISSON FINISHED ----------------------------
    
    Solving Quantum Mechanics ---- (quantum regions without density only)
    
    
    Solving Quantum Mechanics ---- (determine k-dispersion only)
    
    
    ********* OUTPUT ***************************************************************
    
    Writing characteristics data(1)...
    Writing characteristics data(2)...
    
    Writing electrostatic potential...
    
    Writing band edges...
    
    Writing Fermi levels...
    
    Writing results from quantum calculations...
    
    Writing carrier densities...
    Writing ionized dopant densities...
    
    ********* FINISHED CALCULATION *************************************************
    
    End time: Wed 2021-09-29, 15:21:42 (+0200)
    Total Poisson Solver Time: 0.013[s]
    Total Quantum Solver Time: 0.007[s]
    Simulator Run Time: 0.73[s]
    
    ================================================================================
    DONE.
    ================================================================================
    

Please contact python@nextnano.com for any issues with this document.
