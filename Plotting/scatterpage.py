''' copyright Chris Wood 2017.
'''

import os
from collections import OrderedDict

from bokeh.plotting import figure, curdoc, ColumnDataSource
from bokeh.models.widgets import Div
from bokeh.layouts import row, column, layout, widgetbox
from bokeh.layouts import widgetbox
from bokeh.models.widgets import Dropdown, Select
from bokeh.models.callbacks import CustomJS
# from bokeh.io import output_server, push

import numpy as np
import pandas

# import filepicker

def getfilelist(dirname):
    files = os.listdir(dirname)
    goodtypes = ['csv', 'xlsx']
    a = list()
    for f in files:
        if f.split(".")[-1] in goodtypes:
        # if f.endswith('csv'):
            a.append(f)
    return a

class scatterpage():

    def __init__(self, datafile=None, datadir=None):

        self.colortable = np.asarray(
            ['#8dd3c7', '#ffffb3', '#bebada', '#fb8072',
             '#80b1d3', '#fdb462', '#b3de69', '#fccde5',
             '#d9d9d9', '#bc80bd', '#ccebc5', '#ffed6f'])

        self.layout = None
        self.excelfile = None
        self.doc = curdoc()
        self.fakedata()
        self.datadir = datadir
        self.page_setup()
        if datadir is not None:
            self.datadir = datadir

    def load_data_file(self, datafile):
        self.datafile = datafile
        if datafile.endswith('xlsx'):
            self.excelfile = pandas.ExcelFile(datafile)
        else:
            self.excelfile = None
            self.df = self.openfile()
            self.load_data()


    def load_data_sheet(self, sheetname):
        self.df = self.excelfile.parse(sheetname)
        self.load_data()

    def load_data(self):
        self.data = self.df_to_dict(self.df)
        self.colnames = list(self.data.keys())
        keys = list(self.data.keys())
        self.xcol = keys[0]
        self.ycol = keys[1]
        self.data['x'] = self.data[self.xcol]
        self.data['y'] = self.data[self.ycol]
        self.colorcol = keys[2]
        self.make_color_array()
        self.sizecol = keys[3]
        self.make_size_array()
        print('done with color array')

    def page_setup(self):
        keys = list(self.data.keys())
        self.settools(
            "tap, crosshair,pan ,wheel_zoom,box_zoom,"
            "undo,redo,reset,save,box_select")

        self.makeplot()
        self.makehdiv()
        self.make_file_picker(self.datadir)
        self.make_sheet_picker()
        self.create_x_dropdown()
        self.create_y_dropdown()
        self.create_color_select()
        self.create_size_select()

        self.createlayout()
        if self.layout:
            self.layout.children[0] = self.inside
        else:
            self.layout = row(self.inside,
                                 sizing_mode='stretch_both')

        self.doc.add_root(self.layout)

    def make_file_picker(self, dirname):
        files = getfilelist(dirname)
        files.insert(0, 'Pick a file')
        self.fileselect = Select(title="Select a file", value=files[0],
                            options=files)

        self.fileselect.on_change("value", self.callbackpicker)


    def callbackpicker(self, attr, old, new):
            print(new, old)
            self.datafile = self.datadir + os.sep + new
            ##need to handle if the sheet is an excel file
            self.load_data_file(self.datafile)
            self.fileselect.value = new
            self.sheetname = "no sheet selected"
            self.page_setup()

    def make_sheet_picker(self):
        try:
            sheets = self.excelfile.sheet_names
        except:
            sheets = list()

        sheets.insert(0, 'Pick a sheet')
        self.sheet_select = Select(title='Select a sheet',
                                   value=sheets[0],
                                   options=sheets)
        self.sheet_select.on_change("value", self.callback_sheetpicker)


    def callback_sheetpicker(self, attr, old, new):
        ### do stuff for when a sheet is selected
        print("New in sheet pick", new)
        print(old)
        self.load_data_sheet(new)
        self.sheet_select.value = new
        self.sheetname = new
        self.page_setup()

    def df_to_dict(self, df):
        keys = list(df.keys())
        r = df.iloc[[0]]
        data = OrderedDict()
        for i, k in enumerate(keys, 1):
            try:
                val = float(r[k])
                data[k] = df[k]
            except:
                print(i, r[k], k)
        return data

    def openfile(self):
        df = pandas.read_csv(self.datafile)
        return df

    def create_x_dropdown(self, value=None):
        menu = []
        for n in self.colnames:
            print(n)
            if n in ['x', 'y']:
                print("Going")
                continue
            menu.append((n, n))
        select = Select(title="X axis:", value=self.xcol,
                                   options=self.colnames)
        # dropdown.callback = self.callbackx
        select.on_change("value", self.callbackx)
        self.xwidgetbox = select

    def create_y_dropdown(self, value=None):
        menu = []
        for n in self.colnames:
            if n in ['x', 'y']:
                continue
            menu.append((n, n))
        select = Select(title="Y axis:", value=self.ycol,
                                   options=self.colnames)

        # dropdown.callback = self.callbacky
        select.on_change("value", self.callbacky)
        self.ywidgetbox = select

    def create_color_select(self, value=None):
        select = Select(title="Color column", value=self.colorcol,
                        options=self.colnames)

        select.on_change("value", self.callbackcolor)
        self.colorselect = select

    def create_size_select(self, value=None):
        select = Select(title="Size column", value=self.sizecol,
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

    def callbackx(self, attr, old, new):
        self.setxcol(new)
        self.data['x'] = self.data[self.xcol]
        self.source.data = self.data
        self.figure.xaxis.axis_label = self.xcol
        # self.makeplot()

    def callbacky(self, attr, old, new):
        self.setycol(new)
        self.data['y'] = self.data[self.ycol]
        self.source.data = self.data
        self.figure.xaxis.axis_label = self.ycol
        # self.makeplot()

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
        try:
            self.figure.xaxis.axis_label = self.xwidgetbox.value
        except:
            pass

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
        try:
            print('I am here')
            self.figure.yaxis.axis_label = self.ywidgetbox.value
        except:
            pass

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

        bins = (dc - colmin) // delt
        bins = bins.astype(np.int8)

        colors = self.colortable[bins]
        self.color_array = colors
        self.data['colors'] = colors


    def make_size_array(self):
        sz = self.data[self.sizecol]
        szmax = np.amax(self.data[self.sizecol])
        szmin = np.amin(self.data[self.sizecol])
        sizescale = 5 + 10 * (sz - szmin) // (szmax - szmin)
        self.size_array = sizescale
        self.data['sizes'] = sizescale

    def makeplot(self):

        title = self.datafile.split("/")[-1] + '\n' + self.sheetname
        self.source = ColumnDataSource(self.data)
        self.x = self.data[self.xcol]
        self.y = self.data[self.ycol]
        self.figure = figure(tools=self.tools,title=title)
        self.plot = self.figure.circle(x='x', y='y',
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

        self.figure.xaxis.axis_label = self.xcol
        self.figure.yaxis.axis_label = self.ycol
        # self.makecallbackx()
        # self.makecallbacky()
        print("plot done")

    def update(self, attr, old, new):

        if new is None:
            return
        index = int(new['1d']['indices'][0])

        try:
            if 'http' in self.df['url24hour'][index]:
                text = '<img src=\"' + self.df['url24hour'][index] + \
                       '" height="512"/>'
        except:
            text = '<img src="null" height="512" alt="No Image available"/>'

        s = self.datarow_to_table(index)
        text += s

        # text = unicode(text)
        self.div.update(text=text)

    def makehdiv(self):
        self.div = Div()
        self.div.text = "<h1>Click points to show data</h1>"

    def updatediv(self, text):
        self.div.text = text

    def make_title_div(self, text):
        d = Div()
        d.text = "<h1>" + text + "</h1>"
        return d

    def make_sheet_div(self, text):
        d = Div()
        d.text = "<h3>" + text + "</h3>"
        return d

    def createlayout(self):
        sheetdiv = self.make_sheet_div(self.sheetname)
        titlediv = self.make_title_div(self.datafile.split("/")[-1])
        filerow = row(self.fileselect, titlediv)
        sheetrow = row(self.sheet_select, sheetdiv)

        w0 = widgetbox(titlediv, sheetdiv, width=600)
        w1 = widgetbox(self.fileselect, self.sheet_select)
        spacerdiv = Div(text='', height=50)
        top = column(w0, w1, spacerdiv)
        # colheaders = column(row(self.fileselect, titlediv),
        #                     row(self.sheet_select, sheetdiv))
        # rowfile = row(colheaders)
        wcol = widgetbox(
                      self.xwidgetbox, self.ywidgetbox,
                      self.colorselect,self.sizeselect)
        col2 = column(self.figure)
        col3 = column(self.div)
        row1 = row(wcol, col2, col3)
        #row2 = row() #self.div)
        # row3 = row(self.colorselect, self.sizeselect)
        self.inside = column(top, row1)
        # self.cols = [col1, col2, col3]
        print("layout done")

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

        x = np.arange(0,1,1)
        y = np.random.uniform(-5,5, len(x))
        c = np.random.uniform(0,10, len(x))
        s = np.random.uniform(0,10, len(x))

        data = dict()
        data['xfake'] = x
        data['yfake'] = y

        data['fakecolors'] = c
        data['fakesizes'] = s
        self.datafile = 'fake data'
        self.data = data
        self.colnames = list(data.keys())
        self.data['x'] = x
        self.data['y'] = y
        self.setxcol('xfake')
        self.setycol('yfake')
        self.setcolorcol('fakecolors')
        self.setsizecol('fakesizes')
        self.make_color_array()
        self.make_size_array()
        self.sheetname = "no sheet"

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