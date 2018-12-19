from PyQt5 import QtWidgets,uic
from PyQt5.QtCore import QThread,pyqtSignal
import threading,queue
import Adafruit_DHT

qu = queue.Queue(1)
pin = 4

def get_data():
    while True:
        h, t = Adafruit_DHT.read_retry(11, pin)
        qu.put((h,t))




class MyThread(QThread):
    signal = pyqtSignal(tuple)
    def __init__(self,data):
        super(MyThread, self).__init__()
        self.data = data

    def run(self):
        self.signal.emit(self.data)
        self.deleteLater()

class MySignal(QtWidgets.QWidget):
    Signal_TwoPar = pyqtSignal(float,float)

class MyAccept(QtWidgets.QWidget):
    def setValue_TwoParameters(self,x,y):
        pass


if __name__ == '__main__':
    DataGettingThread = threading.Thread(target=get_data)
    DataGettingThread.start()

    DataUpdattingThread = threading.Thread()

    app = QtWidgets.QApplication([])
    dlg = uic.loadUi("HTsensor_record.ui")

    dlg.﻿TemperatureValue.display("34.7")


    dlg.show()
    app.exec()