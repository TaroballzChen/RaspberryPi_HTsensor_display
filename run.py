from PyQt5 import QtWidgets,uic
import Adafruit_DHT

sensor = Adafruit_DHT.DHT11


if __name__ == '__main__':

    app = QtWidgets.QApplication([])
    dlg = uic.loadUi("HTsensor_record.ui")

    dlg.show()
    app.exec()