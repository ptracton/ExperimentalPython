import PyQt5
import matplotlib
import matplotlib.pyplot
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg


class QtMpl(FigureCanvasQTAgg):
    '''
    '''

    def __init__(self, parent):

        self.fig, self.axes = matplotlib.pyplot.subplots()

        FigureCanvasQTAgg.__init__(self, self.fig)
        self.setParent(parent)

        #self.axes = self.fig.add_subplot(111)
        self.axes.set_ylabel("Money")
        self.axes.set_xlabel("Dates")
        self.axes.set_title('Movie Revenue by Month')

        # we define the widget as expandable
        FigureCanvasQTAgg.setSizePolicy(self,
                                        PyQt5.QtWidgets.QSizePolicy.Expanding,
                                        PyQt5.QtWidgets.QSizePolicy.Expanding)
        # notify the system of updated policy
        FigureCanvasQTAgg.updateGeometry(self)

    def addBars(self, x=None, revenue=None, budget=None, year=None):
        """
        Add a bar to the graph
        """

        # Clear figure for new plt
        self.axes.cla()

        self.axes.set_title('Movie Revenue and Budget by Month for {}'.format(year))

        # add the new bars to the clear plot
        width = 0.35
        revenue_bars = self.axes.bar(
            x=x, height=revenue, width=0.35, color='SkyBlue', label="Revenue")
        budget_bars = self.axes.bar(
            x=x, height=budget, width=0.35, color='IndianRed', label="Budget")

        self.axes.legend()
        # update the plot display
        # http://stackoverflow.com/questions/4098131/matplotlib-update-a-plot
        self.fig.canvas.draw()
        return
