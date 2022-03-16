# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 10:56:11 2022

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