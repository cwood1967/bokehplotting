''' copyright Chris Wood 2017.
'''

import os

from bokeh.plotting import figure, curdoc, ColumnDataSource
from bokeh.models.widgets import Div
from bokeh.layouts import row, column
from bokeh.layouts import widgetbox
from bokeh.models.widgets import Dropdown, Select
from bokeh.models.callbacks import CustomJS
from bokeh.io import output_server, push

import numpy as np
import pandas

# import filepicker

def getfilelist(dirname):
    files = os.listdir(dirname)
    return files

class scatterpage():

    def __init__(self, datafile=None, datadir=None):

        self.colortable = np.asarray(
            ['#8dd3c7', '#ffffb3', '#bebada', '#fb8072',
             '#80b1d3', '#fdb462', '#b3de69', '#fccde5',
             '#d9d9d9', '#bc80bd', '#ccebc5', '#ffed6f'])

        self.layout = None
        self.doc = curdoc()
        self.fakedata()
        self.datadir = datadir
        self.page_setup()
        if datadir is not None:
            self.datadir = datadir
        #     self.make_file_picker(datadir)
        #     col1 = column(self.fileselect)
        #     #self.main_layout = row(col1)
        #     self.doc.add_root(col1)
        # else:
        #     self.datadir = None
        #     if datafile is not None:
        #         self.load_data_file(datafile)
        #         self.page_setup()
            # print self.data



    def load_data_file(self, datafile):
        self.datafile = datafile
        self.df = self.openfile()
        self.data = self.df_to_dict(self.df)
        self.colnames = self.data.keys()
        keys = self.data.keys()
        self.xcol = keys[0]
        self.ycol = keys[1]
        self.colorcol = keys[3]
        self.make_color_array()
        self.sizecol = keys[4]
        self.make_size_array()

    def page_setup(self):

        keys = self.data.keys()

        self.settools(
            "tap, crosshair,pan ,wheel_zoom,box_zoom,"
            "undo,redo,reset,save,box_select")

        self.makeplot()
        self.makehdiv()
        self.make_file_picker(self.datadir)
        self.create_x_dropdown()
        self.create_y_dropdown()
        self.create_color_select()
        self.create_size_select()

        w = [self.setxcol, self.setycol, self.setcolorcol, self.setsizecol]
        index = 0
        # for i, k in enumerate(keys):
        #     if "url" not in k:
        #         print(index, i, k)
        #         w[index](k)
        #         index += 1
        #     else:
        #         print("no", index, i, k)
        #     if index >= len(w):
        #         break

        self.createlayout()
        if self.layout:
            self.layout.children[0] = self.inside
        else:
            self.layout = column(self.inside)

        #self.doc.remove_root(self.layout)

        #self.doc.clear()

        self.doc.add_root(self.layout)
        # output_server()

    def make_file_picker(self, dirname):
        files = getfilelist(dirname)
        print(files)
        self.fileselect = Select(title="Select a file", value=files[0],
                            options=files)

        self.fileselect.on_change("value", self.callbackpicker)


    def callbackpicker(self, attr, old, new):
            print(new, old)
            self.datafile = self.datadir + os.sep + new
            self.df = self.openfile()
            self.data = self.df_to_dict(self.df)
            self.colnames = self.data.keys()
            self.load_data_file(self.datafile)
            self.page_setup()


    def df_to_dict(self, df):
        keys = df.keys()
        data = dict()
        for k in keys:
            if 'url' not in k:
                data[k] = df[k]

        return data

    def openfile(self):
        print(self.datafile)
        df = pandas.read_csv(self.datafile)
        return df

    def create_x_dropdown(self, value=None):
        menu = []
        for n in self.colnames:
            menu.append((n, n))
        dropdown = select = Select(title="X axis:", value=self.colnames[3],
                                   options=self.colnames)
        dropdown.callback = self.callbackx
        self.xwidgetbox = dropdown

    def create_y_dropdown(self, value=None):
        menu = []
        for n in self.colnames:
            menu.append((n, n))
        dropdown  = Select(title="Y axis:", value=self.colnames[2],
                                   options=self.colnames)

        dropdown.callback = self.callbacky
        self.ywidgetbox = dropdown

    def create_color_select(self, value=None):
        select = Select(title="Color column", value=self.colnames[0],
                        options=self.colnames)

        select.on_change("value", self.callbackcolor)
        self.colorselect = select

    def create_size_select(self, value=None):
        select = Select(title="Size column", value=self.colnames[1],
                        options=self.colnames)

        select.on_change("value", self.callbacksize)
        self.sizeselect = select

    def callbackcolor(self, attr, old, new):

        print("in callbackcolor", new)
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


    def setxcol(self, xcol, value=None):
        self.xcol = xcol
        #self.xwidgetbox.value = value

    def setycol(self, ycol, value=None):
        self.ycol = ycol
        #self.ywidgetbox.value = value

    def setcolorcol(self, colorcol, value=None):
        print(colorcol, value)
        self.colorcol = colorcol
        # self.colorselect.value = value
        self.make_color_array()

    def setsizecol(self, sizecol, value=None):
        self.sizecol = sizecol
        #self.sizeselect.value = value
        self.make_size_array()

    def make_color_array(self):
        print("color--col", self.colorcol)
        dc = self.data[self.colorcol]
        colmax = np.amax(dc)
        colmin = np.amin(dc)
        delt = 1.*(colmax - colmin)/(len(self.colortable) - 1)

        bins = (dc - colmin) / delt
        bins = bins.astype(np.int8)

        colors = self.colortable[bins]
        self.color_array = colors
        self.data['colors'] = colors


    def make_size_array(self):
        sz = self.data[self.sizecol]
        szmax = np.amax(self.data[self.sizecol])
        szmin = np.amin(self.data[self.sizecol])
        sizescale = 10 + 15 * (sz - szmin) / (szmax - szmin)
        self.size_array = sizescale
        self.data['sizes'] = sizescale

    def makeplot(self):
        self.source = ColumnDataSource(self.data)
        self.x = self.data[self.xcol]
        self.y = self.data[self.ycol]
        self.figure = figure(tools=self.tools)
        self.plot = self.figure.circle(x=self.xcol, y=self.ycol,
                                       source=self.source,
                                       size='sizes',
                                       fill_color='colors',
                                       fill_alpha=0.95,
                                       line_color='#888888',
                                       line_width=.5,
                                       selection_line_color='blue',
                                       nonselection_fill_color='colors',
                                       nonselection_fill_alpha=0.65)

        print(self.plot, self.figure)
        self.plot.data_source.on_change('selected', self.update)
        self.makecallbackx()
        self.makecallbacky()
        print "plot done"

    def update(self, attr, old, new):

        if new is None:
            return
        index = int(new['1d']['indices'][0])

        text = '<img src=\"' + self.df['url24hour'][
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
        col1 = column(self.fileselect,
                      self.xwidgetbox, self.ywidgetbox,
                      self.colorselect,self.sizeselect)
        col2 = column(self.figure)
        col3 = column(self.div)
        row1 = row(col1, col2, col3)
        #row2 = row() #self.div)
        # row3 = row(self.colorselect, self.sizeselect)
        self.inside = column(row1)
        # self.cols = [col1, col2, col3]
        print "layout done"

    def datarow_to_table(self, index):

        namelist = self.colnames
        s = '''<style>
            table {
                border-collapse: collapse;
            }
            table, th, td {
            border: 1px solid black;
            font-size: 16px;
        }
        th, td {
            padding: 8px;
            text-align: left;
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

    def fakedata(self):

        x = np.arange(0,10,.1)
        y = np.random.uniform(-5,5, len(x))
        c = np.random.uniform(0,10, len(x))
        s = np.random.uniform(0,10, len(x))

        data = dict()
        data['xfake'] = x
        data['yfake'] = y
        data['fakecolors'] = c
        data['fakesizes'] = s
        self.data = data
        self.colnames = data.keys()
        self.setxcol('xfake')
        self.setycol('yfake')
        self.setcolorcol('fakecolors')
        self.setsizecol('fakesizes')
        self.make_color_array()
        self.make_size_array()

## colors for color table
'''
#8dd3c7
#ffffb3
#bebada
#fb8072
#80b1d3
#fdb462
#b3de69
#fccde5
#d9d9d9
#bc80bd
#ccebc5
#ffed6f
'''