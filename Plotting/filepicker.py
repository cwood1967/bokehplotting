
import os

from bokeh.models.widgets import Div, Select
from bokeh.layouts import row, column


class filepicker():
    def __init__(self, dirname):
        self.filelist = getfilelist()
        self.row = make_file_picker(self.dirname)

def getfilelist(dirname):
    files = os.listdir(dirname)
    return files

def callbackpicker(attr, old, new):
    pass

def make_file_picker(dirname):
    files = getfilelist(dirname)

    fileselect = Select(title="Select a file", value=files[0],
                        options=files)

    fileselect.on_change("value", callbackpicker)
    row1 = row(fileselect)
