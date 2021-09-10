"""
Definition of settings in the GUI
"""
from collections import OrderedDict

QC_STATUS_FAIL = 0
QC_STATUS_PASS = 1
BTN_DEFAULT_STYLESHEET = "color: white; background:rgb(60, 63, 65);"
BTN_PASS_STYLESHEET = "color: black; background-color: green;"
BTN_FAIL_STYLESHEET = "color: white; background-color: red;"
DELAY = 100  # msec to wait after pass/fail was clicked
REQUIRED_TABLE_COLUMNS = ['ID','imgpath', 'QC', 'comment']
HIDE_TIMER = True  # Hides the "time spent" timer!
SELECTION_COLOR = {
    "blue": "#0000FF",
    "green": "#008000",
    "coral": "#ff7f50",
    "navy": "#000080",
    "orange": "#ffa500",
    "olive": "#808000",
}

# Settings for the MPL Widget
PICKERRADIUS = 1

MARKER_SIZE_DEFAULT = 12
MARKER_SIZE_HIGHLIGHT = 30