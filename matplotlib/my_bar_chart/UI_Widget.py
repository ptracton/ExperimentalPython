import PyQt5
import PyQt5.QtCore
import PyQt5.QtWidgets

import QtMpl

class UI_Widget(PyQt5.QtWidgets.QDialog):
    def __init__(self, parent=None):
        """
        This is the layer that handles creating and displaying the various
        UI elements in the central window
        """
        super(UI_Widget, self).__init__(parent)
        vbox = PyQt5.QtWidgets.QVBoxLayout()

        label = PyQt5.QtWidgets.QLabel("Simple UI Template")
        self.button = PyQt5.QtWidgets.QPushButton("Simple UI Button")

        self.matplot = QtMpl.QtMpl(parent=parent)
        
        vbox.addWidget(label)
        vbox.addWidget(self.button)
        vbox.addWidget(self.matplot)
        
        self.setLayout(vbox)
        return
