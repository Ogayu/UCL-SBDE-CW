# -*- coding: utf-8 -*-
"""ALL - SA_Morris.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nUVWtR1y_dC9YNbfMAnmLHAdCTmwJPlo
"""

pip install SALib

from SALib.analyze import morris
from SALib.util import read_param_file
from SALib.plotting.morris import horizontal_bar_plot, covariance_plot, \
    sample_histograms
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from google.colab import files

def fullprint(*args, **kwargs):
  from pprint import pprint
  import numpy
  opt = numpy.get_printoptions()
  numpy.set_printoptions(threshold=numpy.inf)
  pprint(*args, **kwargs)
  numpy.set_printoptions(**opt)

#IMPORT DATA
problem = read_param_file('/content/drive/My Drive/Colab Notebooks/Integrated Design/parameter_file.txt')
#model_input = np.loadtxt('/content/drive/My Drive/Colab Notebooks/Integrated Design/model_input.txt')
#model_output = np.loadtxt('/content/drive/My Drive/Colab Notebooks/Integrated Design/model_output.txt')
data = np.loadtxt('/content/drive/My Drive/Colab Notebooks/Integrated Design/2166.txt')
print("data ndim: ", data.ndim)
print("data shape:", data.shape)
print("data size: ", data.size)

D=problem["num_vars"] #number of variables
print(data[:,0:D].shape)

rows=data.shape[0] #number of inputs/outputs
print("rows: ",rows)
n=divmod(rows,D+1)[0]
print("n: ",n)
model_input=data[:,0:14][0:n*(D+1),:]
model_input.shape

D=problem["num_vars"] #number of variables
for x in [0,1]: #x=1 kgCO2, x=2 %comf_t
  # Prepare data for the analysis for each system
  filename = 'SA Morris '
  rows=data.shape[0] #number of inputs/outputs
  n=divmod(rows,D+1)[0]
  model_input=data[:,0:14][0:n*(D+1),:]
  model_output=data[:,D+x:D+1+x][0:n*(D+1),:]
  print(filename)
  # Perform the sensitivity analysis
  Si = morris.analyze(problem, model_input, model_output, conf_level=0.95,
                      print_to_console=True)
  #create plots
  fig1, (ax1, ax2) = plt.subplots(1, 2)
  #ax1.set_title(filename)
 # ax2.set_title(filename)
  if x == 0:
    horizontal_bar_plot(ax1, Si, {}, sortby='mu_star', unit=r"kgCO2")
    covariance_plot(ax2, Si, {}, unit=r"kgCO2")
    filename_update=filename+"_kgCO2"
  else:
    horizontal_bar_plot(ax1, Si, {}, sortby='mu_star', unit=r"%ComfTime")
    covariance_plot(ax2, Si, {}, unit=r"%ComfTime")
    filename_update=filename+"_ComfTime"
  ax1.set_title(filename_update)
  ax2.set_title(filename_update)  
  #save and download plots  
  plt.savefig(filename_update)
  files.download(filename_update+".png")
  plt.close()