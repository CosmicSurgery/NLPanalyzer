from bokeh.io import curdoc
from bokeh.themes import built_in_themes
from bokeh.models.layouts import Tabs

import pandas as pd
import os

from tab1 import tab1



PATH = os.getcwd()
df = pd.read_hdf(os.path.join(PATH,"vis","demo.h5"))

tab1 = tab1(df)

tabs = Tabs(tabs = [tab1])

curdoc().add_root(tabs)
