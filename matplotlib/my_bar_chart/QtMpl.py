
import PyQt5
import matplotlib
import matplotlib.pyplot
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg


class QtMpl(FigureCanvasQTAgg):
    '''
    '''

    def __init__(self, parent):

        #self.fig = matplotlib.figure.Figure()
        #self.axes = matplotlib.pyplot.gca()

        self.fig, self.axes = matplotlib.pyplot.subplots()
        
        FigureCanvasQTAgg.__init__(self, self.fig)
        self.setParent(parent)

        # we define the widget as expandable
        FigureCanvasQTAgg.setSizePolicy(self, PyQt5.QtWidgets.QSizePolicy.Expanding,
                                        PyQt5.QtWidgets.QSizePolicy.Expanding)
        # notify the system of updated policy
        FigureCanvasQTAgg.updateGeometry(self)

    def addBars(self, x=None, y=None, title=None):
        """
        Add a bar to the graph
        """
        print("addBar {} {} {}".format(x, y, title))
        bars = self.axes.bar(x, y)
        
        # http://stackoverflow.com/questions/4098131/matplotlib-update-a-plot
        self.fig.canvas.draw()
        return
        
