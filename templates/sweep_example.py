from pathlib import Path

import numpy as np

import nextnanopy as nn

# Prototype input file whose variables are swept. QW_WIDTH and QW_SEPARATION
# set the geometry of the double quantum well.
input_file = Path(__file__).parent / "input files" / "DoubleQuantumWell_6nm_demo.nnp"

# Each variable maps to the values it should take; the sweep runs one
# simulation per combination of the two.
sweep_variables = {
    "QW_WIDTH": np.linspace(4.0, 8.0, 3),  # width of both quantum wells (nm)
    "QW_SEPARATION": np.linspace(2.0, 6.0, 3),  # separation of the wells (nm)
}

sweep = nn.Sweep(sweep_variables, input_file)
sweep.save_sweep(temp=True) # saves the sweep to a temporary directory

# show log=False means that the log of each simulation is not printed to the console
# by default the failed simulation does not raise an exception
# but you can change this behavior with the `convergenceCheck` argument
sweep.execute_sweep(show_log=False, convergenceCheck=True, convergence_check_mode="terminate")
