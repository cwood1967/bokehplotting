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
print file
p = scatterpage.scatterpage(datafile=None, datadir=dirpath)

# p.setxcol('sumhobbit24hour')
# p.setycol('sumlinc24hour')
# p.setcolorcol('cxcfile-hobbit24hour')
# p.setsizecol('area24hour')
# p.settools("tap, crosshair,pan ,wheel_zoom,box_zoom,undo,redo,reset,save,box_select")
#
# p.makeplot()
# p.makehdiv()
# p.create_x_dropdown()
# p.create_y_dropdown()
# p.create_color_select()
# p.create_size_select()
# print p.callbackx
# print "hello"
# p.createlayout()
#
# curdoc().add_root(p.layout)

