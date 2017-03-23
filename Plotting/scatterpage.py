''' copyright Chris Wood 2017.
'''


from bokeh.plotting import figure, curdoc, ColumnDataSource
from bokeh.models.widgets import Div
from bokeh.layouts import row, column
from bokeh.layouts import widgetbox
from bokeh.models.widgets import Dropdown, Select
from bokeh.models.callbacks import CustomJS

import numpy as np
import pandas


class scatterpage():

    def __init__(self, datafile):
        self.datafile = datafile
        self.df = self.openfile()
        self.data = self.df_to_dict(self.df)
        self.colnames = self.data.keys()
        # print self.data

    def df_to_dict(self, df):
        keys = df.keys()
        data = dict()
        for k in keys:
            data[k] = df[k]

        return data

    def openfile(self):
        df = pandas.read_csv(self.datafile)
        return df

    def create_x_dropdown(self):
        menu = []
        for n in self.colnames:
            menu.append((n, n))
        dropdown = select = Select(title="X axis:", value=self.colnames[3],
                                   options=self.colnames)
        dropdown.callback = self.callbackx
        self.xwidgetbox = dropdown

    def create_y_dropdown(self):
        menu = []
        for n in self.colnames:
            menu.append((n, n))
        dropdown  = Select(title="Y axis:", value=self.colnames[4],
                                   options=self.colnames)

        dropdown.callback = self.callbacky
        self.ywidgetbox = dropdown

    def create_color_select(self):
        select = Select(title="Color column", value=self.colnames[0],
                        options=self.colnames)

        select.on_change("value", self.callbackcolor)
        self.colorselect = select

    def create_size_select(self):
        select = Select(title="Size column", value=self.colnames[1],
                        options=self.colnames)

        select.on_change("value", self.callbacksize)
        self.sizeselect = select

    def callbackcolor(self, attr, old, new):

        print self.color_array[0:10]
        self.setcolorcol(new)
        self.data['colors'] = self.color_array
        self.source.data = self.data

    def callbacksize(self, attr, old, new):
        self.setsizecol(new)
        self.data['size'] = self.size_array
        self.source.data = self.data

    def makecallbackx(self):

        code = '''
            var column = cb_obj.value;
            plot.glyph.x.field = column;
            source.trigger('change');
            console.log(cb_obj.value);
            console.log(source);
        '''

        self.callbackx = CustomJS(args=dict(plot=self.plot,
                                            source=self.source,
                                            figure=self.figure),
                                  code=code)

    def makecallbacky(self):

        code = '''
            var column = cb_obj.value;
            plot.glyph.y.field = column;
            source.trigger('change');
        '''

        self.callbacky = CustomJS(args=dict(plot=self.plot,
                                            source=self.source,
                                            figure=self.figure),
                                  code=code)

    def settools(self, tools):
        self.tools = [tools]


    def setxcol(self, xcol):
        self.xcol = xcol

    def setycol(self, ycol):
        self.ycol = ycol

    def setcolorcol(self, colorcol):
        self.colorcol = colorcol
        self.make_color_array()

    def setsizecol(self, sizecol):
        self.sizecol = sizecol
        self.make_size_array()

    def make_color_array(self):
        cr = np.zeros(len(self.df), dtype=np.float32)
        for i in range(len(cr)):
            cr[i] = self.df[self.colorcol][i]

        print cr[0:10]
        colmax = np.amax(self.df[self.colorcol])
        colmin = np.amin(self.df[self.colorcol])

        cr = 200 *(cr - colmin)/(colmax - colmin)
        cg = np.flip(cr, 0)
        print cr[0:10]
        colors = np.asarray([
                                "#%02x%02x%02x" % (50+int(r), 50+ int(g), 20) for r, g
                                in zip(cr, cg)])

        print colors[0:10]
        self.color_array = colors
        self.data['colors'] = colors


    def make_size_array(self):
        sz = self.df[self.sizecol]
        szmax = np.amax(self.df[self.sizecol])
        szmin = np.amin(self.df[self.sizecol])
        sizescale = 10 + 15 * (sz - szmin) / (szmax - szmin)
        self.size_array = sizescale
        self.data['sizes'] = sizescale

    def makeplot(self):
        self.source = ColumnDataSource(self.data)
        self.x = self.df[self.xcol]
        self.y = self.df[self.ycol]
        self.figure = figure(tools=self.tools)
        self.plot = self.figure.circle(x=self.xcol, y=self.ycol,
                                       source=self.source,
                                       size='sizes',
                                       fill_color='colors',
                                       fill_alpha=0.9,
                                       line_color=None,
                                       selection_line_color='blue',
                                       nonselection_fill_color='colors',
                                       nonselection_fill_alpha=0.5)

        self.plot.data_source.on_change('selected', self.update)
        self.makecallbackx()
        self.makecallbacky()
        print "plot done"

    def update(self, attr, old, new):

        if new is None:
            return
        index = int(new['1d']['indices'][0])

        text = '<img src=\"' + self.source.data['url24hour'][
            index] + '" height="256"/>'
        s = self.datarow_to_table(index)
        text += '\n'
        text += s
        # text = unicode(text)
        self.div.update(text=text)

    def makehdiv(self):
        self.div = Div()
        self.div.text = "<h1>Nothing</h1>"

    def updatediv(self, text):
        self.div.text = text

    def createlayout(self):
        row1 = row(self.figure, self.div)
        row2 = row(self.xwidgetbox, self.ywidgetbox)
        row3 = row(self.colorselect, self.sizeselect)
        self.layout = column(row1, row2, row3)
        print "layout done"

    def datarow_to_table(self, index):

        namelist = self.colnames
        s = '''<style>
            table {
                border-collapse: collapse;
            }
            table, th, td {
            border: 1px solid black;
        }
        </style>\n'''
        s += '<table>\n'
        for name in namelist:
            v = self.df[name][index]
            try:
                s += '<tr><td>%s</td><td>%.3f</td></tr>\n' % (name, float(v))
            except:
                pass
        s += '</table>'
        return s





