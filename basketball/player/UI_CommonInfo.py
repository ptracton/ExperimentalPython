
import PyQt5
import PyQt5.QtWidgets

class UI_CommonInfo(PyQt5.QtWidgets.QDialog):
    """
    Display Common Player Information
    """
    def __init__(self, parent=None):
        super(UI_CommonInfo, self).__init__(parent)

        self.topLayout = PyQt5.QtWidgets.QVBoxLayout()

        self.hbox1 = PyQt5.QtWidgets.QHBoxLayout()

        idLabel = PyQt5.QtWidgets.QLabel("ID Number:")
        self.playerID = PyQt5.QtWidgets.QLabel("")
        self.hbox1.addWidget(idLabel)
        self.hbox1.addWidget(self.playerID)
        
        birthDateLabel = PyQt5.QtWidgets.QLabel("Birthdate:")
        self.playerBirthDate = PyQt5.QtWidgets.QLabel("")
        self.hbox1.addWidget(birthDateLabel)
        self.hbox1.addWidget(self.playerBirthDate)

        heightLabel = PyQt5.QtWidgets.QLabel("Height:")
        self.playerHeight = PyQt5.QtWidgets.QLabel("")
        self.hbox1.addWidget(heightLabel)
        self.hbox1.addWidget(self.playerHeight)

        
        weightLabel = PyQt5.QtWidgets.QLabel("Weight:")
        self.playerWeight = PyQt5.QtWidgets.QLabel("")
        self.hbox1.addWidget(weightLabel)
        self.hbox1.addWidget(self.playerWeight)
        
        self.topLayout.addLayout(self.hbox1)
        return

    def getLayout(self):
        return self.topLayout
