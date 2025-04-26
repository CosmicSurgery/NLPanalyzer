from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Legend
from bokeh.models.widgets import RadioButtonGroup, Select, CheckboxGroup
from bokeh.layouts import column, row
from bokeh.models.layouts import TabPanel, Tabs

def tab1():


    top = figure(x_axis_type='datetime', frame_height=300, frame_width=1000, title = 'Cumulative Sum')
    

    layout = column()
    tab = TabPanel(child=layout, title = 'This is a test')

    return tab