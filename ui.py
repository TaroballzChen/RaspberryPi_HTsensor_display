from PyQt5 import QtWidgets

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()


    def initUI(self):
        self.setGeometry(100,100,800,600)
        self.setWindowTitle("Humidity & Temperature display")

    