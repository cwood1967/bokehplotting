import os

from bokeh.plotting import curdoc
import scatterpage

file = 'hobbit01.csv'

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

