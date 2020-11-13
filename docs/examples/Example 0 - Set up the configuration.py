#!/usr/bin/env python
# coding: utf-8

# # Welcome to nextnanopy !
# 
# ## About this example: nextnano configuration
# 
# If you have a nextnano software license, the first thing you want to do is to set up the configuration so you can execute input files easily.
# 
# On the other hand, most of the nextnanopy features can be used without the need of a valid nextnano license, except you want to execute input files via Python. For that, it is recommendable to set up once your configuration at the beginning.
# 
# ## What is the configuration?
# 
# The configuration mainly includes the paths to the executables, the license files, the default output folder, etc. 
# 
# This configuration is stored as a file called .nextnanopy-config and it will be located at your home directory (usually C:\Users\Your_User\.nextnanopy-config)
# 
# When you import nextnanopy for the first time, it will automatically generate the configuration file with few default parameters. If this file already exists, it won't modify it.
# 
# You can set up this configuration file only once and you don't need to worry about it anymore, except when you renovate your license or update the nextnano version.
# 

# ## Let's import nextnanopy before setting up the configuration

# In[1]:


import nextnanopy as nn


# ## How can I access to the configuration?
# 
# The configuration can be access via:
# 
# ```python
# nextnano.config
# ```
# 
# To get a given option from a section (nextnano++, nextnano3 or nextnano.NEGF), you can use the get method
# 
# ```python
# nextnano.config.get(section, option)
# ```
# 
# To get all the options from a section, use get method:
# 
# ```python
# nextnano.config.get_options(section)
# ```
# 
# You can also get the location of the configuration file:
# 
# ```python
# nextnano.config.fullpath
# ```

# In[2]:


nn.config


# In[3]:


nn.config.get('nextnano++','exe')


# In[4]:


nn.config.get_options('nextnano++')


# In[5]:


nn.config.fullpath


# ## Where do I find each path?
# 
# If you have activated your license via nextnanomat, the easiest way is to go the nextnanomat\Tools\Options.
# You can find in the Simulation tab, the executable paths for each nextnano software (nextnano++, nextnano3, nextnano.NEGF, nextnano.MSB).
# 
# Similarly, in the Material database and the Licenses tabs, you find the database and license paths.
# 
# 
# ## How can I set each option?
# 
# If you want to set each option, you can simply do:
# 
# ```python
# nextnano.config.set(section,option,value)
# ```
# 
# Please, use absolute paths to avoid any possible problem and be aware of backslash or forwardslash depending on your OS. We highly recommend to use 'r' in front of the path as shown below to avoid any syntax conflict in python.
# 
# Note that after setting the options, you have to save the configuration via
# 
# ```python
# nextnano.config.save()
# ```
# 
# You also can save the configuration elsewhere with a new name like here:
# 
# ```python
# nextnano.config.save(r'C:\new_path\random_name.nextnanopy-config')
# ```
# 
# In the latest case, nextnanopy will always look for the configuration file in your HOME directory and NOT this one. It can seem useless to save your own configuration file, although it can be useful in some cases that we will show later in this example.

# In[6]:


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


# In[7]:


nn.config


# ## Execute input file with the default configuration
# 
# By loading an input file with InputFile class (for more information, see Example2), it will automatically load as well the configuration file. You can access it via:
# 
# ```python
# my_input = nextnanopy.InputFile('example.in')
# my_input.config
# ```
# 
# When you want to execute the input file, 
# 
# ```python
# my_input.execute()
# ```
# 
# It will automatically detect the nextnano product (nextnano++, nextnano3 or nextnano.NEGF) and will load the corresponding configuration parameters.

# In[8]:


my_input = nn.InputFile(r'E:\junliang.wang\datafiles\nextnano++\example.in')
my_input.config


# In[9]:


my_input.execute()


# ## Execute with different parameters
# 
# ### Method 1: use another configuration file
# 
# If you want to execute an input file with another configuration file, you can do
# 
# ```python
# my_input = nextnanopy.InputFile('example.in',configpath=r'C:\new_path\random_name.nextnanopy-config')
# my_input.config
# ```
# 
# For this specific input file, it will use the user-defined configuration file for executing the simulation.
# 
# This feature can be useful if you have different versions of nextnano installed and you would like to use a given version for a set of input files.
# 
# ### Method 2: without any configuration file
# 
# You can pass one or more specific arguments like outputdirectoy or threads to the execute method like below:
# 
# ```python
# my_input.execute(outputdirectory=r'C:\Users\jun-liang.wang\Downloads', threads=4)
# ```

# In[10]:


my_input.execute(outputdirectory=r'C:\Users\jun-liang.wang\Downloads', threads=4)


# ## Reset the configuration to default
# 
# If you want to reset to the default configuration, you can simply do
# 
# ```python
# nextnano.config.to_default()
# nextnano.config.save()
# ```
# 
# Remember that you need to save the file after the modification.

# In[11]:


nn.config.to_default() # not saved automatically
nn.config.save() # save the default values
print(nn.config)


# Please, contact python@nextnano.com for any issue with this example.
