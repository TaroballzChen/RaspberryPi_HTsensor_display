from PyQt5 import QtWidgets,uic
from PyQt5.QtGui import QPixmap,QFont
import threading,queue
import Adafruit_DHT
import datetime
import os
import csv

qu = queue.Queue(1)
pin = 4
moderate_temperature = 20

def get_data():
    while True:
        h, t = Adafruit_DHT.read_retry(22, pin)
        qu.put((h,t))

def send_data():
    record_flag = 0
    while True:
        data = qu.get()
        hum = data[0]
        tem = data[1]
        dlg.HumidityValue.display("%.1f"%hum)
        dlg.TemperatureValue.display("%.1f"%tem)
        dlg.StatusLabel.setPixmap(Not_OK_pic)
        nowTime = datetime.datetime.now().strftime("%m%d-%H:%M:%S")
        min = int(datetime.datetime.now().minute)
        sec = int(datetime.datetime.now().second)
        if (min % 5 == 4 and sec >= 58) or (min %5 ==0 and sec in [0,1]):
            if record_flag == 0:
                currentRowCount = dlg.tableWidget.rowCount()
                dlg.tableWidget.insertRow(dlg.tableWidget.rowCount())
                dlg.tableWidget.setItem(currentRowCount, 0, QtWidgets.QTableWidgetItem(nowTime))
                dlg.tableWidget.setItem(currentRowCount, 1, QtWidgets.QTableWidgetItem(str(tem)))
                dlg.tableWidget.setItem(currentRowCount, 2, QtWidgets.QTableWidgetItem(str(hum)))
                dlg.tableWidget.setItem(currentRowCount, 3, QtWidgets.QTableWidgetItem("OK"))
                record_temp(tem)
                SaveDatabase()
                record_flag =1
            else:
                continue
        else:
            record_flag =0

def Temperature_status(temp):
    old_temperateure = temp
    def Record_old_temp(now_temp):
        nonlocal old_temperateure
        if now_temp >= moderate_temperature and old_temperateure >= moderate_temperature and now_temp <= moderate_temperature +10 and old_temperateure <= moderate_temperature + 10 :
            dlg.StatusLabel.setPixmap(OK_pic)

        elif now_temp >= moderate_temperature +10:
            dlg.StatusLabel.setPixmap(Not_OK_pic)
        else:
            dlg.StatusLabel.setPixmap(Not_OK_pic)
        dlg.StatusLabel.setScaledContents(True)
        print("old:",old_temperateure,"now:",now_temp)
        old_temperateure = now_temp


    return Record_old_temp


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
    dlg = uic.loadUi("HTsensor_record_new.ui")
    dlg.Date.setText("%s"%datetime.datetime.now().strftime("%Y/%m/%d"))
    dlg.Date.setFont(QFont("Arial",22,QFont.Black))
    Not_OK_pic = QPixmap("icon/NO.png")
    OK_pic = QPixmap("icon/OK.png")
    Logo_pic = QPixmap("icon/logo.png")
    record_temp = Temperature_status(qu.get()[1])
    dlg.Logo.setPixmap(Logo_pic)
    dlg.Logo.setScaledContents(True)
    DataUpdattingThread = threading.Thread(target=send_data)
    DataUpdattingThread.start()
    dlg.show()
    app.exec()