import numpy as np
from PyQt5.QtCore import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from matplotlib.figure import Figure


PICKERRADIUS = 1

class MplCanvas(FigureCanvasQTAgg):
    transmit_data_index = pyqtSignal(int)

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self._color_highlight = np.array([255, 37, 0]) / 255

        self._marker_size_default = 12
        self._marker_size_highlight = 20

        def onpick(event):
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

        def onclick(event):
            print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
                  ('double' if event.dblclick else 'single', event.button,
                   event.x, event.y, event.xdata, event.ydata))

        super(MplCanvas, self).__init__(self.fig)

    def updatePlot(self, xdat, ydat, selected_index, xlabel=None, ylabel=None):
        self.axes.cla()
        C = [[0, 0, 1] for _ in range(len(xdat))]
        S = [self._marker_size_default for _ in range(len(xdat))]
        C[selected_index] = self._color_highlight
        S[selected_index] = self._marker_size_highlight
        self.axes.scatter(xdat, ydat, picker=True, pickradius=PICKERRADIUS, s=S, c=C)
        self.axes.set_xlabel(xlabel)
        self.axes.set_ylabel(ylabel)
        self.figure.canvas.draw()

    def updatePlotMultiColumns(self, xdat, ydat, selected_index, xlabel=None, ylabel=None, colors=None):
        self.axes.cla()

        num_cols = ydat.shape[1]
        for i in range(num_cols):
            C = [ colors[i] for _ in range(len(xdat))]
            S = [self._marker_size_default for _ in range(len(xdat))]
            C[selected_index] = self._color_highlight
            S[selected_index] = self._marker_size_highlight
            self.axes.scatter(xdat, ydat[:,i], picker=True, pickradius=PICKERRADIUS, s=S, c=C)
        self.axes.set_xlabel(xlabel)
        self.axes.set_ylabel(ylabel)
        self.figure.canvas.draw()


    def refreshPlot(self, selected_index):
        # retrive current data
        xdat, ydat = zip(*self.axes.collections[0].get_offsets())
        self.axes.cla()
        C = [[0, 0, 1] for _ in range(len(xdat))]
        S = [self._marker_size_default for _ in range(len(xdat))]

        C[selected_index] = self._color_highlight
        S[selected_index] = self._marker_size_highlight
        self.axes.scatter(xdat, ydat, picker=True, pickradius=PICKERRADIUS, s=S, c=C)
        self.figure.canvas.draw()
