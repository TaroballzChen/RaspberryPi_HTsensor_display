from PyQt5 import QtWidgets,uic
import threading,queue
import Adafruit_DHT
import datetime
import os
import csv

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
        nowTime = datetime.datetime.now().strftime("%m%d-%H:%M:%S")
        min = int(datetime.datetime.now().minute)
        sec = int(datetime.datetime.now().second)
        if (min % 5 == 4 and sec >= 58) or (min %5 ==0 and sec in [0,1]):
            currentRowCount = dlg.tableWidget.rowCount()
            dlg.tableWidget.insertRow(dlg.tableWidget.rowCount())
            dlg.tableWidget.setItem(currentRowCount, 0, QtWidgets.QTableWidgetItem(nowTime))
            dlg.tableWidget.setItem(currentRowCount, 1, QtWidgets.QTableWidgetItem(str(tem)))
            dlg.tableWidget.setItem(currentRowCount, 2, QtWidgets.QTableWidgetItem(str(hum)))
            dlg.tableWidget.setItem(currentRowCount, 3, QtWidgets.QTableWidgetItem("OK"))
            SaveDatabase()

def SaveDatabase():
    FileName = "%s.csv"%(datetime.datetime.now().strftime("%Y%m%d"))
    if os.path.isfile(FileName):
        mode(FileName,"a")
    else:
        mode(FileName,"w")


def mode(filename,mode):
    rowcount = dlg.tableWidget.rowCount()
    with open(filename, mode, newline="", ) as csv_file:
        writer = csv.writer(csv_file, dialect='excel', lineterminator='\n')
        row_data = []
        for column in range(4):
            item = dlg.tableWidget.item(rowcount - 1, column)
            if item is not None:
                row_data.append(item.text())
            else:
                row_data.append("")
        writer.writerow(row_data)


if __name__ == '__main__':
    DataGettingThread = threading.Thread(target=get_data)
    DataGettingThread.start()

    app = QtWidgets.QApplication([])
    dlg = uic.loadUi("HTsensor_record.ui")
    DataUpdattingThread = threading.Thread(target=send_data)
    DataUpdattingThread.start()
    dlg.show()
    app.exec()