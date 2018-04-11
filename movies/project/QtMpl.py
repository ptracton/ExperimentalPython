
import PyQt5
import matplotlib
import matplotlib.pyplot
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg


class QtMpl(FigureCanvasQTAgg):
    '''
    '''

    def __init__(self, parent):

        self.fig = matplotlib.figure.Figure()

        FigureCanvasQTAgg.__init__(self, self.fig)
        self.setParent(parent)

        self.fig, self.axes = matplotlib.pyplot.subplots()
        
        #self.axes = self.fig.add_subplot(111)
        self.axes.set_ylabel("Money")
        self.axes.set_xlabel("Dates")
        self.axes.set_title('Movie Revenue by Month')

        # we define the widget as expandable
        FigureCanvasQTAgg.setSizePolicy(self, PyQt5.QtWidgets.QSizePolicy.Expanding,
                                        PyQt5.QtWidgets.QSizePolicy.Expanding)
        # notify the system of updated policy
        FigureCanvasQTAgg.updateGeometry(self)

    def addBar(self, x=None, y=None, title=None):
        """
        Add a bar to the graph
        """

        self.axes.bar(x=x, height=y)
        
         # http://stackoverflow.com/questions/4098131/matplotlib-update-a-plot
        self.fig.canvas.draw()
        return
        
    def addLine(self, x, y, title):
        self.fig.gca().xaxis.set_major_formatter(
            mdates.DateFormatter('%m/%d/%Y'))
        self.fig.gca().xaxis.set_major_locator(mdates.DayLocator())
        self.line_list.append(
            self.axes.plot_date(x, y, label=title, xdate=True))
        self.axes.legend()

        # http://stackoverflow.com/questions/4098131/matplotlib-update-a-plot
        self.fig.canvas.draw()
        return
