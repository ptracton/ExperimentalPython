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

        vboxLayout = PyQt5.QtWidgets.QVBoxLayout()
        vboxLayout.addLayout(hboxPlayerName)

        self.commonInfo = UI_CommonInfo.UI_CommonInfo()
        vboxLayout.addLayout(self.commonInfo.getLayout())
        self.setLayout(vboxLayout)
        return
