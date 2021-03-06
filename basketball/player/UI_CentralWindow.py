import PyQt5
import PyQt5.QtWidgets

import UI_CommonInfo

class UI_CentralWindow(PyQt5.QtWidgets.QDialog):
    """
    This class hold the UI elements
    """

    def __init__(self, parent=None):
        super(UI_CentralWindow, self).__init__(parent)

        # Enter the player's name
        playerNameLabel = PyQt5.QtWidgets.QLabel("Enter Player's Name")
        self.playerNameLineEdit = PyQt5.QtWidgets.QLineEdit()
        self.playerNamePushButton = PyQt5.QtWidgets.QPushButton("Look Up Player")

        hboxPlayerName = PyQt5.QtWidgets.QHBoxLayout()
        hboxPlayerName.addWidget(playerNameLabel)
        hboxPlayerName.addWidget(self.playerNameLineEdit)
        hboxPlayerName.addWidget(self.playerNamePushButton)

        self.imageLabel = PyQt5.QtWidgets.QLabel("Image Goes Here")
        self.pixmap = PyQt5.QtGui.QPixmap()
        
        hboxLayout = PyQt5.QtWidgets.QHBoxLayout()
        hboxLayout.addWidget(self.imageLabel)

        self.commonInfo = UI_CommonInfo.UI_CommonInfo()
        hboxLayout.addLayout(self.commonInfo.getLayout())

        self.playerDataTable = PyQt5.QtWidgets.QTableWidget()
        self.playerDataTable.setRowCount(2)
        self.playerDataTable.setColumnCount(27)
        #        self.playerDataTable.setHorizontalHeaderLabels(["Header 1", "Header 2", "Header 3"])
                
        vboxLayout = PyQt5.QtWidgets.QVBoxLayout()
        vboxLayout.addLayout(hboxPlayerName)
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addWidget(self.playerDataTable)
        
        self.setLayout(vboxLayout)
        return

    def updateImage(self, imageFileName=None):
        """
        Display the image in the GUI
        """
        try:
            self.pixmap.load(imageFileName)
        except:
            return
        
        scaledPixmap = self.pixmap.scaled(self.imageLabel.size(),
                                          PyQt5.QtCore.Qt.KeepAspectRatio)
        self.imageLabel.setPixmap(self.pixmap)
        self.imageLabel.setScaledContents(False)
        return    
