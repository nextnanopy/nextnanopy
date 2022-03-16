# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 10:56:11 2022

@author: takuma.sato
"""

import nextnanopy as nn
import os

inputPath = r'\input files\convergenceTest_nn3.in'
# inputPath = 'convergenceTest_nnp.in'
# inputPath = 'convergenceTest_negf.mxml'

inputPath = os.path.abspath(inputPath)
input_file = nn.InputFile(inputPath)

input_file.execute(convergenceCheck=True)

print("I'm still running")