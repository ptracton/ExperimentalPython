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
        """
        Respond to the primary button being pushed
        """

        # Read the name from the UI
        playerName = self.centralWidget.playerNameLineEdit.text()


        # Create an instance of NBA_Player which gets information for us
        player = NBA_Player.NBA_Player(fullName=playerName)

        # If there is no player of this name, return before updating the GUI
        if player.isValid() is False:
            return

        player.getImage()
        
        self.centralWidget.commonInfo.playerID.setText(str(player.commonInfoList[0]))
        self.centralWidget.commonInfo.playerBirthDate.setText(player.commonInfoList[6])
        self.centralWidget.commonInfo.playerHeight.setText(player.commonInfoList[10])
        self.centralWidget.commonInfo.playerWeight.setText(player.commonInfoList[11])

        self.centralWidget.commonInfo.playerSeason.setText(str(player.commonInfoList[12]))
        self.centralWidget.commonInfo.playerJersey.setText(str(player.commonInfoList[13]))
        self.centralWidget.commonInfo.playerPosition.setText(player.commonInfoList[14])
        self.centralWidget.updateImage(player.imageFileName)

        self.centralWidget.playerDataTable.setHorizontalHeaderLabels(player.careerHeaders)
        self.centralWidget.playerDataTable.setRowCount(len(player.careerStatsList))

        row = 0
        column = 0
        for line in player.careerStatsList:
            for cell in line:
                #print("{} {} {}".format(row, column, player.careerStatsList[row][column]))
                self.centralWidget.playerDataTable.setItem(row, column, PyQt5.QtWidgets.QTableWidgetItem(str(player.careerStatsList[row][column])))
                column = column + 1
            row = row + 1
            column = 0
        return
