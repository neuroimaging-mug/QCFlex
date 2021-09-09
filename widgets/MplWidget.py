import numpy as np
from PyQt5.QtCore import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from matplotlib.figure import Figure

from settings import PICKERRADIUS, MARKER_SIZE_DEFAULT, MARKER_SIZE_HIGHLIGHT


class MplCanvas(FigureCanvasQTAgg):
    transmit_data_index = pyqtSignal(int)

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self._color_highlight = np.array([255, 37, 0]) / 255
        self.init = False

        def onpick(event):
            if event.mouseevent.dblclick:
                return

            collection = event.artist

            xdata, ydata = zip(*collection.get_offsets())

            if len(event.ind) > 1:
                print("Clicked multiple indices, selecting first of them...")
                ind = event.ind[0]
            else:
                ind = event.ind
            ind = int(ind) #
            self.fig.canvas.flush_events()
            self.fig.canvas.draw()
            print('on pick line:', np.array([xdata[ind], ydata[ind]]).T)
            self.transmit_data_index.emit(ind)

        self.pid = self.fig.canvas.mpl_connect('pick_event', onpick)

        super(MplCanvas, self).__init__(self.fig)

    def updatePlot(self, xdat, ydat, selected_index, xlabel=None, ylabel=None):
        self.axes.cla()
        C = [[0, 0, 1] for _ in range(len(xdat))]
        S = [MARKER_SIZE_DEFAULT for _ in range(len(xdat))]
        C[selected_index] = self._color_highlight
        S[selected_index] = MARKER_SIZE_HIGHLIGHT
        self.axes.scatter(xdat, ydat, picker=True, pickradius=PICKERRADIUS, s=S, c=C)
        self.axes.scatter(xdat[selected_index], ydat[selected_index], s=S[selected_index], c=C[selected_index])
        self.axes.set_xlabel(xlabel)
        self.axes.set_ylabel(ylabel)
        self.figure.canvas.draw()

        # Flag which signals the refresh function which update to call
        self.init = True

    def updatePlotMultiColumns(self, xdat, ydat, selected_index, xlabel=None, ylabel=None, colors=None):
        self.axes.cla()

        num_cols = ydat.shape[1]
        for i in range(num_cols):
            C = [ colors[i] for _ in range(len(xdat))]
            S = [MARKER_SIZE_DEFAULT for _ in range(len(xdat))]
            C[selected_index] = self._color_highlight
            S[selected_index] = MARKER_SIZE_HIGHLIGHT
            self.axes.scatter(xdat, ydat[:,i], picker=True, pickradius=PICKERRADIUS, s=S, c=C)
            self.axes.scatter(xdat[selected_index], ydat[selected_index,i], s=S[selected_index], c=C[selected_index])
        self.axes.set_xlabel(xlabel)
        self.figure.canvas.draw()


    def refreshPlot(self, selected_index):
        # retrive current data
        if len(self.axes.collections) > 0:
            xdat, ydat = zip(*self.axes.collections[0].get_offsets())
        else:
            print("No data selected... Skipping!")
            return
        self.axes.cla()
        C = [[0, 0, 1] for _ in range(len(xdat))]
        S = [MARKER_SIZE_DEFAULT for _ in range(len(xdat))]

        C[selected_index] = self._color_highlight
        S[selected_index] = MARKER_SIZE_HIGHLIGHT
        self.axes.scatter(xdat, ydat, picker=True, pickradius=PICKERRADIUS, s=S, c=C)
        self.figure.canvas.draw()
