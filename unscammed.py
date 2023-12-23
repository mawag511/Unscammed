from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
from scam_check import message_check
from resources import logo_resource
import sys, time

''' Splash Screen'''
class SplashScreen(QDialog):
    def __init__(self):
        super(SplashScreen, self).__init__()
        loadUi("./GUIs/SplashScreenGUI.ui", self)
        self.setWindowTitle("UNSCAMMED")
        self.setWindowIcon(QIcon("./resources/assets/icon.png"))
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


class Worker(QThread):
    progressChanged = pyqtSignal(int)
    def run(self):
        for count in range(2):
            self.progressChanged.emit(count)
            self.sleep(1)
        self.progressChanged.emit(-1)


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
    def loading(self):
        self.movie = QMovie("./resources/assets/loading.gif")
        self.Loading.setScaledContents(True)
        self.Loading.setMovie(self.movie)
        self.movie.start()


    def check_message(self):
        self.input = self.UserInput.toPlainText()
        if self.input != "" and len(self.input.strip()):
            self.worker = Worker()
            self.worker.progressChanged.connect(
                lambda: (self.Loading.show(), self.loading()))
            self.worker.finished.connect(
                lambda: (self.Loading.hide(), self.open_results()))
            self.worker.start() 
            self.WarningLabel.setText("")
            self.results = message_check(str(self.input))
        else:
            self.WarningLabel.setText("Please insert a message to verify!")


    def open_results(self):
        if self.input != "" and len(self.input.strip()):
            self.stackedWidget.setCurrentWidget(self.SL_results)
            self.Results.setAlignment(Qt.AlignCenter)
            self.Results.setText(self.results)
            self.CheckedMessage.setText(self.input)
            self.UserInput.setText("")
    

    ## to drag frame
    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton:
            self.m_flag=True
            self.m_Position=event.globalPos()-self.pos() 
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))
            
    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:  
            self.move(QMouseEvent.globalPos()-self.m_Position)
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