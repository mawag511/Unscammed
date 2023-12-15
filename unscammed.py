from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.uic import loadUi
import sys, time

from scam_locator import message_check
from resources import logo_resource

app = QtWidgets.QApplication(sys.argv)
widgets = QStackedWidget()


class SplashScreen(QDialog):
    def __init__(self):
        super(SplashScreen, self).__init__()
        loadUi("./GUIs/SplashScreenGUI.ui", self)
        self.setFixedHeight(495)
        self.setFixedWidth(760)
        self.timer = QTimer()
        self.timer.timeout.connect(self.loading)
        self.timer.start(60)
       #widgets.setWindowFlags(Qt.FramelessWindowHint)   <-- to fix
   
    def loading(self):
        self.timer.stop()
        time.sleep(3)
        main_menu = MainMenu()
        widgets.addWidget(main_menu)
        widgets.setCurrentIndex(widgets.currentIndex()+1)
        widgets.setWindowTitle("UNSCAMMED")
        #widgets.setWindowIcon(QIcon("icon.png"))   <-- to fix
        widgets.setFixedHeight(695)
        widgets.setFixedWidth(880) 


class MainMenu(QDialog):
    def __init__(self):
        super(MainMenu, self).__init__()
        loadUi("./GUIs/MainMenuGUI.ui", self)
        
        self.SpamDetectionBTN.clicked.connect(self.go_to_scam_locator)

    def go_to_scam_locator(self):
        scam_locator = ScamLocator()
        widgets.addWidget(scam_locator)
        widgets.setCurrentIndex(widgets.currentIndex()+1)


class ScamLocator(QDialog):
    def __init__(self):
        super(ScamLocator, self).__init__()
        loadUi("./GUIs/ScamLocatorSubmissionGUI.ui", self)
        self.SubmitBTN.clicked.connect(self.message_check)
        self.GoBackBTN.clicked.connect(self.go_back_to_main_menu)

    def message_check(self):
        global input
        global results
        input = self.UserInput.toPlainText()

        if input != "":
            self.WarningLabel.setText("")
            results = message_check(str(input))
            self.go_to_scam_locator_res()
        else:
            self.WarningLabel.setText("Please insert a message to verify!")
   
    def go_to_scam_locator_res(self):
        scam_locator_res = ScamLocatorResults()        
        widgets.addWidget(scam_locator_res)
        widgets.setCurrentIndex(widgets.currentIndex()+1)
        scam_locator_res.Results.setText(results)
        scam_locator_res.CheckedMessage.setText(input)

    def go_back_to_main_menu(self):
        main_menu = MainMenu()
        widgets.addWidget(main_menu)
        self.close()
        widgets.setCurrentIndex(widgets.currentIndex()+1)
      

class ScamLocatorResults(QDialog):
    def __init__(self):
        super(ScamLocatorResults, self).__init__()
        loadUi("./GUIs/ScamLocatorResultsGUI.ui", self)
        self.GoBackBTN.clicked.connect(self.go_back_to_scam_locator)

    def go_back_to_scam_locator(self):
        scam_locator = ScamLocator()        
        widgets.addWidget(scam_locator)
        widgets.setCurrentIndex(widgets.currentIndex()+1)
 
def main():
    splash_screen = SplashScreen()
    widgets.addWidget(splash_screen)

    widgets.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
    widgets.show()
    sys.exit(app.exec_() )


if __name__ == "__main__":
   main()