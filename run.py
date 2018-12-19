from PyQt5 import QtWidgets,uic
import threading,queue
import Adafruit_DHT
import datetime

qu = queue.Queue(1)
pin = 4

def get_data():
    while True:
        h, t = Adafruit_DHT.read_retry(11, pin)
        qu.put((h,t))

def send_data():
    while True:
        data = qu.get()
        hum = data[0]
        tem = data[1]
        dlg.HumidityValue.display(str(hum))
        dlg.TemperatureValue.display(str(tem))
        nowTime = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        min = int(datetime.datetime.now().minute)
        sec = int(datetime.datetime.now().second)
        if min % 5 == 4 and sec >= 57:
            currentRowCount = dlg.tableWidget.rowCount()
            dlg.tableWidget.insertRow(dlg.tableWidget.rowCount())
            dlg.tableWidget.setItem(currentRowCount, 0, QtWidgets.QTableWidgetItem(nowTime))
            dlg.tableWidget.setItem(currentRowCount, 1, QtWidgets.QTableWidgetItem(str(tem)))
            dlg.tableWidget.setItem(currentRowCount, 2, QtWidgets.QTableWidgetItem(str(hum)))
            dlg.tableWidget.setItem(currentRowCount, 3, QtWidgets.QTableWidgetItem("OK"))

if __name__ == '__main__':
    DataGettingThread = threading.Thread(target=get_data)
    DataGettingThread.start()

    app = QtWidgets.QApplication([])
    dlg = uic.loadUi("HTsensor_record.ui")
    DataUpdattingThread = threading.Thread(target=send_data)
    DataUpdattingThread.start()
    dlg.show()
    app.exec()