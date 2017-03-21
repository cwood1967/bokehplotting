from bokeh.plotting import figure, show, output_file, curdoc, ColumnDataSource
from bokeh.charts import Scatter
from bokeh.models.images import ImageSource
from bokeh.models import HoverTool, TapTool, CustomJS, Circle
from bokeh.models.widgets import Div
from bokeh.layouts import row, column
import numpy as np
import pandas
import os

images = os.listdir("static/images")

for i, image in enumerate(images):
    images[i] = "Plotting/static/images/" + image

print images

ni = len(images)

N = 400
x = np.random.random(size=N) * 100
y = np.random.random(size=N) * 100

desc = []
for i in range(len(x)):
    desc.append("Desc " + str(i))

imagelist = np.random.randint(0,ni,N)
img = []
for i, rn in enumerate(imagelist):
    img.append(images[rn])

npimages = np.asarray(images)
radii = 10 + np.random.random(size=N)*np.amax(x)*.1
colors = np.asarray([
    "#%02x%02x%02x" % (int(r), int(g), 150) for r, g in zip(50+2*x, 30+2*y)])

# df = pandas.DataFrame({'x':x, 'y':y, 'image':npimages[imagelist],
#                        'radius':radii, 'colors':colors})


print len(x), len(y), len(img), len(desc)
source = ColumnDataSource(
        data=dict(
            x=x.tolist(),
            y=y.tolist(),
            desc=desc,
            imgs=img,
            colors=colors.tolist()
            # fonts=['<i>italics</i>',
            #        '<pre>pre</pre>',
            #        '<b>bold</b>',
            #        '<small>small</small>',
            #        '<del>del</del>'
            #        ]
        )
    )


hover = HoverTool(
        tooltips="""
        <div>
            <div>
                <img
                    src="@imgs" height="64" alt="@imgs"
                    style="float: left; margin: 0px 30px 30px 0px;"
                    border="2"
                ></img>
            </div>
            <div>
                <span style="font-size: 17px; font-weight: bold;">@desc</span>
                <span style="font-size: 15px; color: #966;">[$index]</span>
            </div>
            <div>
                <span>@fonts{safe}</span>
            </div>
            <div>
                <span style="font-size: 15px;">Location</span>
                <span style="font-size: 10px; color: #696;">($x, $y)</span>
            </div>
        </div>
        """
    )

TOOLS="tap, crosshair,pan ,wheel_zoom,box_zoom,undo,redo,reset,save,box_select,poly_select,lasso_select,"

def update(attr, old, new):
    # print 'attr',attr
    # print 'old', old
    print 'new',new

    if new is None:
        return
    index = int(new['1d']['indices'][0])
    print "dsfdffdf" , type(source.data['x'][index])
    xt = source.data['x'][index]
    yt = source.data['y'][index]
    mt = source.data['imgs'][index]

    print "index ", index

    print imagelist[index]
    text = '<img src=\"' + images[imagelist[index]] + '" width="128"/>'
    text += '<ul>'
    text += '<li>' + str(xt) + '</li>'
    text += '<li>' + str(yt) + '</li>'
    text += '<li>' + str(mt) + '</li>'
    text == '</ul>'
    print text
    div.update(text=text)


fd = figure(tools=[hover, TOOLS])

scatter = fd.circle('x', 'y', size=radii,
                     fill_color=colors, fill_alpha=0.9,
                     line_color=None,
                     selection_line_color="firebrick", source=source,
                    nonselection_fill_color="colors",
                    nonselection_fill_alpha=0.5,
                     )

div = Div()
div.text = '<img src=\"' + images[0] + '" width="128"/>'
p = row(fd, div)


#output_file("color_scatter.html", title="color_scatter.py example")
#show(p)
curdoc().add_root(p)




print scatter.data_source.properties()
print "testing"
scatter.data_source.on_change('selected', update)
# scatter.data_source.
