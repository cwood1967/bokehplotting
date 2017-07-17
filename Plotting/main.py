import os

from bokeh.plotting import curdoc
from bokeh.layouts import row, column


import scatterpage
#import filepicker
from os.path import dirname, join


dirpath = os.path.dirname(__file__)
filename = 'hobbit01.csv'
#fp = filepicker.make_file_picker(dirname(__file__))

# curdoc().add_root(fp)
file = join(dirname(__file__), filename)
print(file)
p = scatterpage.scatterpage(datafile=None, datadir=dirpath)



