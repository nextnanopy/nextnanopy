Example for experienced users\* 1: ExecutionQueue for parallel execution
========================================================================

\*Examples for experienced users are recommended for users with prior experience in python
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

About this example
------------------

In Example 4: Use Sweep to automate execution it is shown how to run few
input files simultaneously using
nextnanopy.Sweep.execute_sweep(parallel_limit = n). Implementation of
the parallelization is based on thread like object
nextanopy.inputs.ExecutionQueue. This example shows how to use this
object directly to parallel several simulations at a time if your goal
doesn’t fall under Sweep

About ExecutionQueue
~~~~~~~~~~~~~~~~~~~~

ExecutionQueue class inherits from threading.thread class. To learn more
about threading visit https://docs.python.org/3/library/threading.html .

The implementation is following: InputFile objects can be added to
waiting queue (ExecutionQueue.waiting_queue). On run, InputFiles from
queue is executed and added to execution pool (ExecutionQueue.started)
until it is full. Whenever some simulations are finished, new InputFile
is poped from waiting queue.

To create ExecutionQueue object

.. code:: ipython3

    from nextnanopy.inputs import ExecutionQueue
    my_queue = ExecutionQueue(parallel_limit = 3, show_log = False)

Folowing parameters can be passed:
''''''''''''''''''''''''''''''''''

limit_parallel: int, optional

::

   number of InputFiles to be executed in parallel (default: 1)
           

terminate_empty : bool, optional

::

   If True, terminates once all added files are executed and logged.
   If you want to add more input files even after execution of all added in the beginning, use termanate_empy = False
   Then the ExecutionQueue has to be stopped manually later (ExecutionQueue.stop())
   default: True
           

convergenceCheck: bool

::

   see convergenceCheck in InputFile
   default: False

\**execution_kwargs:

::

   parameters to be taken by InputFile.execute() (show_log for example)

Following commands can be used:
'''''''''''''''''''''''''''''''

add(*input_files)

::

   adds InputFiles to queue

start()

::

   start the thread (i.e. execution)
   see threading.Thread.start()

stop()

::

   stop the thread (once all added files are executed)
   only necessary if termanate_empty = True

join()

::

   wait for the finish of the thread (see threading.Thread.join())

To use this object you will need to create the InputFiles

.. code:: ipython3

    import nextnanopy as nn

.. code:: ipython3

    example_path = r'.\input_files/sweep_example.in'
    input_file1 = nn.InputFile(example_path)
    input_file2 = nn.InputFile(example_path)
    input_file3 = nn.InputFile(example_path)
    input_file4 = nn.InputFile(example_path)
    input_file5 = nn.InputFile(example_path)
    input_file6 = nn.InputFile(example_path)

Now we will modify and safe input files with different names (overwrite
= False)

.. code:: ipython3

    input_file1.set_variable(name = 'BIAS', value = 1.0)
    input_file1.save()
    input_file2.set_variable(name = 'SIZE', value = 83)
    input_file2.save()
    input_file3.set_variable(name = 'SIZE', value = 91)
    input_file3.save()
    input_file4.set_variable(name = 'ALLOY', value = 0.1)
    input_file4.save()
    input_file5.set_variable(name = 'ALLOY',value = 0.2)
    input_file5.set_variable(name = 'SIZE',value = 0.6)
    input_file5.save()
    input_file6.set_variable(name = 'NUMEV', value = 12)
    input_file6.save()
    




.. parsed-literal::

    '.\\input_files\\sweep_example_5.in'



*Note: different input_file objects should be created. Modifying the
same InputFile object n times will not work.*

*Hint: you can use deepcopy in some cases to simplify the code.*

Now we will add these objects to the waiting queue

.. code:: ipython3

    my_queue.add(input_file1,input_file2,input_file3,input_file4,input_file5,input_file6)

And start the queue

.. code:: ipython3

    my_queue.start()


.. parsed-literal::

    
    Remaining simulations in the queue:  5
    
    Remaining simulations in the queue:  4
    
    Remaining simulations in the queue:  3
    
    Remaining simulations in the queue:  2
    
    Remaining simulations in the queue:  1
    
    Remaining simulations in the queue:  0
    
    Waiting queue is empty, all execution and logging are finished
    

How *not to* use ExecutionQueue
-------------------------------

It is not recommended to use ExecutionQueue in cases when Sweep is
applicable. If you want to run the same input file modifying one
parameter n times, or if you want to modify k different parameters and
simulate all combinations of subspace - please, use nextnanopy.Sweep.
The Sweep implementation of parallel execution is written in a way to
avoid usual problems of threading in python.

How to use ExecutionQueue
-------------------------

Here are some examples when Sweep is not applicable and ExecutionQueue
is recommended.

1. You want to simulate in parallel input file changing 3 variables
   A,B,C… but not all combinations of them: Example: 1. A=1,B=1,C = 3 A
   = 2,B=1,C = 3 A = 2.5,B = 2, C = 1

2. You want to postprocess/visualise some results of simulation while
   others are still in process

3. You want to create and add to the queue new simulations based on the
   output of finished from the same queue. (here terminate_empty = False
   is recommended. Do not forget to do ExecutionQueue.stop() in the end)

Some comments on time efficiency
--------------------------------

Be aware that some nextnano solvers parallelize computations internally
in threads (controlled by –threads in nextnanopy config). To avoid
unexpected behaviour and not desirable decrease of simulation speed use
the rule: parallel_limit*threads<= number of physical cores of the
mahcine

\*if you run this example by yourselve, do not forget to delete created
input files in examples/input_files folder (all examples with number at
the end)

Please contact python@nextnano.com for any issues with this document.

