# -*- coding: utf-8 -*-
#%%
import os
import ast
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import neurokit2 as nk
import cvxopt as cv

base_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(base_dir)

#%%

