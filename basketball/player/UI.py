import PyQt5
import PyQt5.QtWidgets

import UI_CentralWindow

import NBA_Player

class UI(PyQt5.QtWidgets.QMainWindow):
    """
    Top Level UI Class
    """

    def __init__(self, parent=None):

        super(UI, self).__init__(parent)

        self.statusBar().showMessage('Status Bar')
        self.setWindowTitle('NBA Player Project')

        # Create our central widget
        self.centralWidget = UI_CentralWindow.UI_CentralWindow()
        self.setCentralWidget(self.centralWidget)

        # Connect signals and handlers
        self.centralWidget.playerNamePushButton.clicked.connect(self.playerNamePushButtonClicked)
        
        # display the UI
        self.show()
        
        return

    def playerNamePushButtonClicked(self):

        playerName = self.centralWidget.playerNameLineEdit.text()
        print(playerName)
        player = NBA_Player.NBA_Player(fullName=playerName)

        self.centralWidget.commonInfo.playerID.setText(str(player.commonInfoList[0]))
        self.centralWidget.commonInfo.playerBirthDate.setText(player.commonInfoList[6])
        self.centralWidget.commonInfo.playerHeight.setText(player.commonInfoList[10])
        self.centralWidget.commonInfo.playerWeight.setText(player.commonInfoList[11])
        
        return
