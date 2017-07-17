import os

from bokeh.plotting import curdoc
from bokeh.layouts import row, column


import scatterpage
#import filepicker
from os.path import dirname, join


filedirpath = os.path.dirname(__file__)
path_split = filedirpath.split(os.sep)
path_split.remove(path_split[-1])
path_split.append('Data')
dirpath = "/".join(path_split)
filename = 'hobbit01.csv'
#fp = filepicker.make_file_picker(dirname(__file__))

# curdoc().add_root(fp)
file = join(dirname(__file__), filename)
print(file)
p = scatterpage.scatterpage(datafile=None, datadir=dirpath)



