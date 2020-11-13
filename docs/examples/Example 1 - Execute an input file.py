#!/usr/bin/env python
# coding: utf-8

# # Welcome to nextnanopy !
# 
# ## About this example: load and execute an input file
# 
# To work with an input file, simply do:
# 
# ```python
# my_input = nextnanopy.InputFile(path_to_file)
# ```
# 
# This object contains all the relevant information of the input file such as the raw text, the variables and the configuration for the execution (see Example 0).
# 
# When you create ```my_input```, the class will first check automatically the type of the input file (nextnano++, nextnano3, nextnano.NEGF or nexntano.MSB). Then, it will get the raw text and extract all variables defined in the file like:
# 
# ```
# $my_var = 3 # in nextnano++
# %my_var = 3 ! in nextnano3
# ```
# 
# Note that loading variables or sweeping parameters are not implemented for nextnano.NEGF nor nextnano.MSB yet.

# In[1]:


import nextnanopy as nn
my_input = nn.InputFile(r'E:\junliang.wang\datafiles\nextnano++\example.in')


# ## What information does it contain?
# 
# ```my_input``` has the following relevant attributes:
# 
# - fullpath (str): path to the input file including the name
# - text (str): return raw text
# - variables (list): list of InputVariable objects
# - config: nextnano configuration (see Example 0)
# 

# In[2]:


print(my_input.fullpath)


# In[3]:


print(my_input.text)


# ## Input variables
# 
# The input variables are stored in ```my_input.variables``` as a list of ```InputVariable``` objects.
# 
# These objects have the following attributes:
# 
# - name (str)
# - value (undefined)
# - unit (str, optional)
# - label (str, optional)
# - comment (str, optional)
# - metadata (dict, optional)
# - text (str): raw text in the input file for a given variable

# In[4]:


print(f"List of variables: {my_input.variables}")


# ### Get a variables
# 
# There are several methods to do so:
# 
# ```python
# my_input.get_variable(name) # method 1 (recommended)
# my_input.variables[name] # method 2 (recommended)
# my_input.variables[index] # method 3
# ```

# ### Let's have a quick look of the variables in this file

# In[5]:


for key, var in my_input.variables.items():
    print(var.text)


# ### Variable line number
# 
# It is an information that you won't probably need, but you can see the line number in the input file where the variable is defined:
# 
# ```python
# my_input.variables['BIAS'].metadata
# ```

# In[6]:


my_input.variables['BIAS'].metadata


# ### Modify the variable
# 
# If you want to modify the value of a given variable, you can do:
# 
# ```python
# my_input.set_variable('BIAS',value=3)
# ```
# 
# You can also change the comment:
# ```python
# my_input.set_variable('BIAS',comment='this is a new comment')
# ```
# 
# You can change both at the same time:
# ```python
# my_input.set_variable('BIAS',value=3,comment='this is a new comment')
# ```

# In[7]:


print(f"Old variable: {my_input.get_variable('BIAS').text}")
my_input.set_variable('BIAS',value=3,comment='this is a new comment')
print(f"New variable: {my_input.get_variable('BIAS').text}")


# ## Save the current file
# 
# ```my_input``` has a method ```save``` which allows you to save the current file.
# 
# ```python
# my_input.save()
# ```
# 
# Note that by default, it won't overwrite the current file such that it will find an unused name (like example_1.in) and save it.
# 
# You can overwrite the current file:
# 
# ```python
# my_input.save(overwrite=True)
# ```
# 
# You can save it in another location and with another name:
# 
# ```python
# my_input.save('new_path\new_input.in')
# ```
# 
# Automatically, ```my_input.fullpath``` is updated if the saving was successful.
# 
# By default, if the new location does not exist, it will create the folder automatically. In order to turn this option off, you can do:
# 
# ```python
# my_input.save('new_path\new_input.in',automkdir=False)
# ```

# In[8]:


help(my_input.save)


# ## Execute the input file
# 
# In order to execute the input file:
# 
# ```python
# my_input.execute()
# ```
# 
# Note that if you have modified one or more variables, you must save the file before execution. 
# 
# The ```execute``` method without any arguments, it will use the configuration stored in ```my_input.config```. As explained in Example 0, it will automatically detect the nextnano product (nextnano++, nextnano3, nextnano.NEGF or nextnano.MSB) and will load the corresponding configuration parameters prior execution.
# 
# The optional arguments are:
# 
# - exe: path to nextnano executable
# - license: path to nextnano license file
# - database: path to nextnano database file
# - outputdirectory: path to output folder
# - Other optional arguments depending of the nextnano product

# In[9]:


my_input.execute()


# ## Sweep an input variable
# 
# Since you can change the input variable dynamically, you can sweep its value and execute the file in a simple loop!
# 
# ```python
# for value in [0, 1, 2]:
#     my_input.set_variable('BIAS',value=value)
#     my_input.save() # remember that by default, overwrite is False.
#     my_input.execute() 
# ```

# Please, contact python@nextnano.com for any issue with this example.
