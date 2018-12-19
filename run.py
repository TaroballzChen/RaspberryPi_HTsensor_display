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
        print((h,t))



class MyThread(QThread):
    signal = pyqtSignal(str)
    def __init__(self,text):
        super(MyThread, self).__init__()
        self.text = text

    def run(self):
        self.signal.emit(self.text)
        self.deleteLater()

class MySignal(QtWidgets.QWidget):
    Signal_TwoPar = pyqtSignal(float,float)

class MyAccept(QtWidgets.QWidget):
    def setValue_TwoParameters(self,x,y):
        pass


if __name__ == '__main__':
    DataGettingThread = threading.Thread(target=get_data)
    DataGettingThread.start()



    app = QtWidgets.QApplication([])
    dlg = uic.loadUi("HTsensor_record.ui")



    dlg.show()
    app.exec()