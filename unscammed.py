from PyQt5.QtGui import  QIcon, QCursor, QMovie
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer
from PyQt5.uic import loadUi
import sys, time

from scam_check import message_check
from resources import logo_resource

''' Splash Screen'''
class SplashScreen(QDialog):
    def __init__(self):
        super(SplashScreen, self).__init__()
        loadUi("./GUIs/SplashScreenGUI.ui", self)
        self.setWindowFlags(Qt.FramelessWindowHint)  
        self.setFixedWidth(815)
        self.setFixedHeight(490)
        self.movie = QMovie("./resources/assets/splash_screen.gif")
        self.movie.setScaledSize(self.size())
        self.timer = QTimer()
        self.label.setMovie(self.movie)
        self.timer.timeout.connect(self.loading)
        self.timer.start(4000)
        self.movie.start()
        
    def loading(self):
        self.timer.stop()
        time.sleep(1)
        window = Main()
        window.show()
        self.close()
      

''' Main Application'''
class Main(QMainWindow):
    ## initialization of all app and first page
    def __init__(self):
        super(Main, self).__init__()
        loadUi("./GUIs/ApplicationGUI.ui", self)
        self.setWindowTitle("UNSCAMMED")
        self.setWindowIcon(QIcon("./resources/assets/icon.png")) 
        self.setFixedWidth(880) 
        self.setFixedHeight(695)
        self.stackedWidget.setCurrentWidget(self.main_menu)

        ## buttons
        self.SpamDetectionBTN.clicked.connect(self.open_clear)
        self.SubmitBTN.clicked.connect(self.check_message)
        self.GoBackBTN.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.main_menu))
        self.GoBackBTN_2.clicked.connect(self.open_clear)

    def open_clear(self):
        self.stackedWidget.setCurrentWidget(self.SL_submission)
        self.WarningLabel.setText("")
        self.UserInput.setAcceptRichText(False)

    ## check user input against ML algorithms
    def check_message(self):
        input = self.UserInput.toPlainText()

        if input != "" and len(input.strip()):
            self.WarningLabel.setText("")
            results = message_check(str(input))
            self.stackedWidget.setCurrentWidget(self.SL_results)
            self.Results.setText(results)
            self.CheckedMessage.setText(input)
            self.UserInput.setText("")
        else:
            self.WarningLabel.setText("Please insert a message to verify!")
    
    ## to drag frame
    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton:
            self.m_flag=True
            self.m_Position=event.globalPos()-self.pos() #Get the position of the mouse relative to the window
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor)) #Change the mouse icon
            
    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:  
            self.move(QMouseEvent.globalPos()-self.m_Position) #Change window position
            QMouseEvent.accept()
                
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag=False
        self.setCursor(QCursor(Qt.ArrowCursor))


## execute app
def main():
    app = QApplication(sys.argv)
    splash_screen = SplashScreen()
    splash_screen.show()
    sys.exit(app.exec_() )

if __name__ == "__main__":
   main()