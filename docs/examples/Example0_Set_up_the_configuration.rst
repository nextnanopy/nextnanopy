Example 0 - Set up the configuration
====================================

About this example: nextnano configuration
------------------------------------------

If you have a nextnano software license, the first thing you want to do
is to set up the configuration so you can execute input files easily.

On the other hand, most of the nextnanopy features can be used without
the need of a valid nextnano license, except you want to execute input
files via Python. For that, it is recommendable to set up once your
configuration at the beginning.

What is the configuration?
--------------------------

The configuration mainly includes the paths to the executables, the
license files, the default output folder, etc.

This configuration is stored as a file called .nextnanopy-config and it
will be located at your home directory (usually C:\\Users\\Your_User\\.nextnanopy-config)

When you import nextnanopy for the first time, it will automatically
generate the configuration file with few default parameters. If this
file already exists, it won’t modify it.

You can set up this configuration file only once and you don’t need to
worry about it anymore, except when you renovate your license or update
the nextnano version.

Let’s import nextnanopy before setting up the configuration
-----------------------------------------------------------

.. code:: ipython3

    import nextnanopy as nn

How can I access to the configuration?
--------------------------------------

The configuration can be access via:

.. code:: python

   nextnano.config

To get a given option from a section (nextnano++, nextnano3 or
nextnano.NEGF), you can use the get method

.. code:: python

   nextnano.config.get(section, option)

To get all the options from a section, use get method:

.. code:: python

   nextnano.config.get_options(section)

You can also get the location of the configuration file:

.. code:: python

   nextnano.config.fullpath

.. code:: ipython3

    nn.config




.. parsed-literal::

    NNConfig(C:\Users\jun-liang.wang\.nextnanopy-config)
    [nextnano++]
    exe = 
    license = 
    database = 
    outputdirectory = 
    threads = 0
    [nextnano3]
    exe = 
    license = 
    database = 
    threads = 0
    outputdirectory = 
    debuglevel = 0
    cancel = -1
    softkill = -1
    [nextnano.NEGF]
    exe = 
    license = 
    database = 
    outputdirectory = 
    threads = 0
    [nextnano.MSB]
    exe = 
    license = 
    database = 
    outputdirectory = 
    debug = 0



.. code:: ipython3

    nn.config.get('nextnano++','exe')




.. parsed-literal::

    ''



.. code:: ipython3

    nn.config.get_options('nextnano++')




.. parsed-literal::

    {'exe': '', 'license': '', 'database': '', 'outputdirectory': '', 'threads': 0}



.. code:: ipython3

    nn.config.fullpath




.. parsed-literal::

    'C:\\Users\\jun-liang.wang\\.nextnanopy-config'



Where do I find each path?
--------------------------

If you have activated your license via nextnanomat, the easiest way is
to go the nextnanomat\\Tools\\Options. You can
find in the Simulation tab, the executable paths for each nextnano
software (nextnano++, nextnano3, nextnano.NEGF, nextnano.MSB).

Similarly, in the Material database and the Licenses tabs, you find the
database and license paths.

How can I set each option?
--------------------------

If you want to set each option, you can simply do:

.. code:: python

   nextnano.config.set(section,option,value)

Please, use absolute paths to avoid any possible problem and be aware of
backslash or forwardslash depending on your OS. We highly recommend to
use ‘r’ in front of the path as shown below to avoid any syntax conflict
in python.

Note that after setting the options, you have to save the configuration
via

.. code:: python

   nextnano.config.save()

You also can save the configuration elsewhere with a new name like here:

.. code:: python

   nextnano.config.save(r'C:\new_path\random_name.nextnanopy-config')

In the latest case, nextnanopy will always look for the configuration
file in your HOME directory and NOT this one. It can seem useless to
save your own configuration file, although it can be useful in some
cases that we will show later in this example.

.. code:: ipython3

    nn.config.set('nextnano++','exe',r'C:\Program Files\nextnano\2020_10_16\nextnano++\bin 64bit\nextnano++_Intel_64bit.exe')
    nn.config.set('nextnano++','license',r'C:\Users\jun-liang.wang\Documents\nextnano\License\License_nnp.lic')
    nn.config.set('nextnano++','database',r'C:\Program Files\nextnano\2020_10_16\nextnano++\Syntax\database_nnp.in')
    nn.config.set('nextnano++','outputdirectory',r'E:\junliang.wang\nextnano\Output')
    
    nn.config.set('nextnano3','exe',r'C:\Program Files\nextnano\2020_10_16\nextnano3\Intel 64bit\nextnano3_Intel_64bit.exe')
    nn.config.set('nextnano3','license',r'C:\Users\jun-liang.wang\Documents\nextnano\License\License_nnp.lic')
    nn.config.set('nextnano3','database',r'C:\Program Files\nextnano\2020_10_16\nextnano3\Syntax\database_nn3.in')
    nn.config.set('nextnano3','outputdirectory',r'E:\junliang.wang\nextnano\Output')
    
    nn.config.set('nextnano.NEGF','exe',r'C:\Program Files\nextnano\nextnanoNEGF_2020_06_22\nextnano.NEGF\nextnano.NEGF.exe')
    nn.config.set('nextnano.NEGF','license',r'C:\Program Files\nextnano\nextnanoNEGF_2020_06_22\License\License_nnQCL.lic')
    nn.config.set('nextnano.NEGF','database',r'C:\Program Files\nextnano\nextnanoNEGF_2020_06_22\nextnano.NEGF\Material_Database.xml')
    nn.config.set('nextnano.NEGF','outputdirectory',r'E:\junliang.wang\nextnano\Output')
    
    nn.config.set('nextnano.MSB','exe',r'C:\Program Files\nextnano\nextnano.MSB_2017_12_20\nextnano\2017_12_20\nextnano.MSB\x86\nextnano.MSB-intel.exe')
    nn.config.set('nextnano.MSB','license',r'C:\Users\jun-liang.wang\Documents\nextnano\License\License_nnMSB.lic')
    nn.config.set('nextnano.MSB','database',r'C:\Program Files\nextnano\nextnano.MSB_2017_12_20\nextnano\2017_12_20\nextnano.MSB\Materials.xml')
    nn.config.set('nextnano.MSB','outputdirectory',r'E:\junliang.wang\nextnano\Output')
    
    nn.config.save() #save permanently

.. code:: ipython3

    nn.config




.. parsed-literal::

    NNConfig(C:\Users\jun-liang.wang\.nextnanopy-config)
    [nextnano++]
    exe = C:\Program Files\nextnano\2020_10_16\nextnano++\bin 64bit\nextnano++_Intel_64bit.exe
    license = C:\Users\jun-liang.wang\Documents\nextnano\License\License_nnp.lic
    database = C:\Program Files\nextnano\2020_10_16\nextnano++\Syntax\database_nnp.in
    outputdirectory = E:\junliang.wang\nextnano\Output
    threads = 0
    [nextnano3]
    exe = C:\Program Files\nextnano\2020_10_16\nextnano3\Intel 64bit\nextnano3_Intel_64bit.exe
    license = C:\Users\jun-liang.wang\Documents\nextnano\License\License_nnp.lic
    database = C:\Program Files\nextnano\2020_10_16\nextnano3\Syntax\database_nn3.in
    threads = 0
    outputdirectory = E:\junliang.wang\nextnano\Output
    debuglevel = 0
    cancel = -1
    softkill = -1
    [nextnano.NEGF]
    exe = C:\Program Files\nextnano\nextnanoNEGF_2020_06_22\nextnano.NEGF\nextnano.NEGF.exe
    license = C:\Program Files\nextnano\nextnanoNEGF_2020_06_22\License\License_nnQCL.lic
    database = C:\Program Files\nextnano\nextnanoNEGF_2020_06_22\nextnano.NEGF\Material_Database.xml
    outputdirectory = E:\junliang.wang\nextnano\Output
    threads = 0
    [nextnano.MSB]
    exe = C:\Program Files\nextnano\nextnano.MSB_2017_12_20\nextnano\2017_12_20\nextnano.MSB\x86\nextnano.MSB-intel.exe
    license = C:\Users\jun-liang.wang\Documents\nextnano\License\License_nnMSB.lic
    database = C:\Program Files\nextnano\nextnano.MSB_2017_12_20\nextnano\2017_12_20\nextnano.MSB\Materials.xml
    outputdirectory = E:\junliang.wang\nextnano\Output
    debug = 0



Execute input file with the default configuration
-------------------------------------------------

By loading an input file with InputFile class (for more information, see
Example2), it will automatically load as well the configuration file.
You can access it via:

.. code:: python

   my_input = nextnanopy.InputFile('example.in')
   my_input.config

When you want to execute the input file,

.. code:: python

   my_input.execute()

It will automatically detect the nextnano product (nextnano++, nextnano3
or nextnano.NEGF) and will load the corresponding configuration
parameters.

.. code:: ipython3

    my_input = nn.InputFile(r'E:\junliang.wang\datafiles\nextnano++\example.in')
    my_input.config




.. parsed-literal::

    NNConfig(C:\Users\jun-liang.wang\.nextnanopy-config)
    [nextnano++]
    exe = C:\Program Files\nextnano\2020_10_16\nextnano++\bin 64bit\nextnano++_Intel_64bit.exe
    license = C:\Users\jun-liang.wang\Documents\nextnano\License\License_nnp.lic
    database = C:\Program Files\nextnano\2020_10_16\nextnano++\Syntax\database_nnp.in
    outputdirectory = E:\junliang.wang\nextnano\Output
    threads = 0
    [nextnano3]
    exe = C:\Program Files\nextnano\2020_10_16\nextnano3\Intel 64bit\nextnano3_Intel_64bit.exe
    license = C:\Users\jun-liang.wang\Documents\nextnano\License\License_nnp.lic
    database = C:\Program Files\nextnano\2020_10_16\nextnano3\Syntax\database_nn3.in
    threads = 0
    outputdirectory = E:\junliang.wang\nextnano\Output
    debuglevel = 0
    cancel = -1
    softkill = -1
    [nextnano.NEGF]
    exe = C:\Program Files\nextnano\nextnanoNEGF_2020_06_22\nextnano.NEGF\nextnano.NEGF.exe
    license = C:\Program Files\nextnano\nextnanoNEGF_2020_06_22\License\License_nnQCL.lic
    database = C:\Program Files\nextnano\nextnanoNEGF_2020_06_22\nextnano.NEGF\Material_Database.xml
    outputdirectory = E:\junliang.wang\nextnano\Output
    threads = 0
    [nextnano.MSB]
    exe = C:\Program Files\nextnano\nextnano.MSB_2017_12_20\nextnano\2017_12_20\nextnano.MSB\x86\nextnano.MSB-intel.exe
    license = C:\Users\jun-liang.wang\Documents\nextnano\License\License_nnMSB.lic
    database = C:\Program Files\nextnano\nextnano.MSB_2017_12_20\nextnano\2017_12_20\nextnano.MSB\Materials.xml
    outputdirectory = E:\junliang.wang\nextnano\Output
    debug = 0



.. code:: ipython3

    my_input.execute()


.. parsed-literal::

    C:\Program Files\nextnano\2020_10_16\nextnano++\bin 64bit
    ================================================================================
    STARTING...
    ================================================================================

    (...)

    ================================================================================
    DONE.
    ================================================================================


Execute with different parameters
---------------------------------

Method 1: use another configuration file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to execute an input file with another configuration file,
you can do

.. code:: python

   my_input = nextnanopy.InputFile('example.in',configpath=r'C:\new_path\random_name.nextnanopy-config')
   my_input.config

For this specific input file, it will use the user-defined configuration
file for executing the simulation.

This feature can be useful if you have different versions of nextnano
installed and you would like to use a given version for a set of input
files.

Method 2: without any configuration file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can pass one or more specific arguments like outputdirectoy or
threads to the execute method like below:

.. code:: python

   my_input.execute(outputdirectory=r'C:\Users\jun-liang.wang\Downloads', threads=4)

.. code:: ipython3

    my_input.execute(outputdirectory=r'C:\Users\jun-liang.wang\Downloads', threads=4)


.. parsed-literal::

    C:\Program Files\nextnano\2020_10_16\nextnano++\bin 64bit
    ================================================================================
    STARTING...
    ================================================================================
    (...)
    ================================================================================
    DONE.
    ================================================================================



Reset the configuration to default
----------------------------------

If you want to reset to the default configuration, you can simply do

.. code:: python

   nextnano.config.to_default()
   nextnano.config.save()

Remember that you need to save the file after the modification.

.. code:: ipython3

    nn.config.to_default() # not saved automatically
    nn.config.save() # save the default values
    print(nn.config)


.. parsed-literal::

    NNConfig(C:\Users\jun-liang.wang\.nextnanopy-config)
    [nextnano++]
    exe = 
    license = 
    database = 
    outputdirectory = 
    threads = 0
    [nextnano3]
    exe = 
    license = 
    database = 
    threads = 0
    outputdirectory = 
    debuglevel = 0
    cancel = -1
    softkill = -1
    [nextnano.NEGF]
    exe = 
    license = 
    database = 
    outputdirectory = 
    threads = 0
    [nextnano.MSB]
    exe = 
    license = 
    database = 
    outputdirectory = 
    debug = 0
    

Please, contact python@nextnano.com for any issue with this example.
