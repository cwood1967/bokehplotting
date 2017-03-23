import os

from bokeh.plotting import figure, curdoc, ColumnDataSource
from bokeh.models.widgets import Div
from bokeh.layouts import row

import numpy as np
import pandas

def datarow_to_table(df, index):

    namelist = df.keys()

    s ='<table>\n'
    for name in namelist:
        v = df[name][index]
        try:
            s += '<tr><td>%s</td><td>%.3f</td></tr>\n' % (name, float(v))
        except:
            pass
    s += '</table>'
    return s

datafile = 'hobbit01.csv'
df = pandas.read_csv(datafile, encoding = 'ascii')
colnames = list(df.columns.values)
minfile = np.amin(df[colnames[0]])
maxfile = np.amax(df[colnames[0]])
print minfile, maxfile
desc = []
for i in range(len(df)):
    desc.append("Desc " + str(i))

#radii = 10 + np.random.random(size=len(df))*np.amax()*.1

cr = np.zeros(len(df), dtype=np.int8)
for i in range(len(cr)):
    cr[i] = df[colnames[0]][i]

cr = 255*cr/maxfile
cg = np.flip(cr, 0)

colors = np.asarray([
    "#%02x%02x%02x" % (int(r), int(g), 20) for r, g in zip(cr, cg)])

print colors
df['colors'] = colors

sizecol = 'maxhobbit24hour'

sz = df[sizecol]
szmax = np.amax(df[sizecol])
szmin = np.amin(df[sizecol])
sizescale = 10 + 15*(sz - szmin)/(szmax - szmin)

# df = pandas.DataFrame({'x':x, 'y':y, 'image':npimages[imagelist],
#                        'radius':radii, 'colors':colors})

source = ColumnDataSource(data=df)
    #     data=dict(
    #         x=x.tolist(),
    #         y=y.tolist(),
    #         desc=desc,
    #         imgs=img,
    #         colors=colors.tolist()
    #         # fonts=['<i>italics</i>',
    #         #        '<pre>pre</pre>',
    #         #        '<b>bold</b>',
    #         #        '<small>small</small>',
    #         #        '<del>del</del>'
    #         #        ]
    #     )
    # )

print type(source.data)
# hover = HoverTool(
#         tooltips="""
#         <div>
#             <div>
#                 <img
#                     src="@url24hour" height="64" alt="@url24hour"
#                     style="float: left; margin: 0px 30px 30px 0px;"
#                     border="2"
#                 ></img>
#             </div>
#             <div>
#                 <span style="font-size: 17px; font-weight: bold;">@slice24hour</span>
#                 <span style="font-size: 15px; color: #966;">[$index]</span>
#             </div>
#             <div>
#                 <span>@fonts{safe}</span>
#             </div>
#             <div>
#                 <span style="font-size: 15px;">Location</span>
#                 <span style="font-size: 10px; color: #696;">($x, $y)</span>
#             </div>
#         </div>
#         """
#     )

TOOLS="tap, crosshair,pan ,wheel_zoom,box_zoom,undo,redo,reset,save,box_select,poly_select,lasso_select,"

div = Div()
def update(attr, old, new):
    # print 'attr',attr
    # print 'old', old
    print 'new',new

    if new is None:
        return
    index = int(new['1d']['indices'][0])
    print(type(source.data))
    print "dsfdffdf" #, source.data['url24hour']
    # xt = source.data['x'][index]
    # yt = source.data['y'][index]
    # mt = source.data['imgs'][index]

    print "index ", index

    text = '<img src=\"' + source.data['url24hour'][index] + '" width="700"/>'
    s = datarow_to_table(source.data, index)
    text += '\n'
    text += s
    # text = unicode(text)
    print type(text)
    print text
    div.update(text=text)


fd = figure(tools=[TOOLS])

scatter = fd.circle(x='sumhobbit24hour', y='area24hour', size=sizescale,
                     fill_color=colors, fill_alpha=0.9,
                     line_color=None,
                     selection_line_color="firebrick", source=source,
                    nonselection_fill_color='colors',
                    nonselection_fill_alpha=0.5,
                     )

div.text = '<img src=\"' + df['url24hour'][0] + '" width="700"/>'
p = row(fd, div)


#output_file("color_scatter.html", title="color_scatter.py example")
#show(p)
curdoc().add_root(p)




print scatter.data_source.properties()
print "testing"
scatter.data_source.on_change('selected', update)
# scatter.data_source.
