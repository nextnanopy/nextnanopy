"""
The option
nextnanopy.InputFile().execute(convergenceCheck=True)
checks if the simulation has converged. If not, nextnanopy warns you and ask if you want to continue to postprocessing.
It is safe to set it to True, as non-converged results are not reliable.

Sample input files under \input files do not converge. You can see how nextnanopy handles the non-convergence.

@author: takuma.sato
"""

import nextnanopy as nn
import os
import pathlib
path = pathlib.Path(__file__).parent.resolve()

input_file = 'input files\convergenceTest_nn3.in'
# input_file = 'input files\convergenceTest_nnp.in'
# input_file = 'input files\convergenceTest_negf.xml'

inputPath = os.path.join(path, input_file)
my_input = nn.InputFile(inputPath)

my_input.execute(convergenceCheck=True)

print("I'm still running")