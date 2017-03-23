import os

from bokeh.plotting import curdoc
import scatterpage
from os.path import dirname, join



filename = 'hobbit01.csv'
file = join(dirname(__file__), filename)
print file
p = scatterpage.scatterpage(file)
p.setxcol('sumhobbit24hour')
p.setycol('sumlinc24hour')
p.setcolorcol('cxcfile-hobbit24hour')
p.setsizecol('area24hour')
p.settools("tap, crosshair,pan ,wheel_zoom,box_zoom,undo,redo,reset,save,box_select")

p.makeplot()
p.makehdiv()
p.create_x_dropdown()
p.create_y_dropdown()
p.create_color_select()
p.create_size_select()
print p.callbackx
print "hello"
p.createlayout()

curdoc().add_root(p.layout)

