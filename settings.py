"""
Definition of settings in the GUI
"""
import matplotlib.colors as mpl

QC_STATUS_FAIL = 0
QC_STATUS_PASS = 1
BTN_DEFAULT_STYLESHEET = "color: white; background:rgb(60, 63, 65);"
BTN_PASS_STYLESHEET = "color: black; background-color: green;"
BTN_FAIL_STYLESHEET = "color: white; background-color: red;"
DELAY = 100  # msec to wait after pass/fail was clicked
REQUIRED_TABLE_COLUMNS = ['PatientID', 'imgpath', 'QC', 'comment']
HIDE_TIMER = True  # Hides the "time spent" timer!
SELECTION_COLOR = {
    "coral": "#ff7f50",
    "navy": "#000080",
    "orange": "#ffa500",
    "olive": "#808000",
    "blue": "#0000FF",
    "green": "#008000",
}
