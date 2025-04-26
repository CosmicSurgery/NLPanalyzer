from bokeh.io import curdoc
from bokeh.themes import built_in_themes
from bokeh.models.layouts import Tabs

from tab1 import tab1


tab1 = tab1()

tabs = Tabs(tabs = [tab1])

curdoc().add_root(tabs)