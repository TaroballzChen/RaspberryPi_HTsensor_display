from RaspberryPi_HTsensor_display.ui import MainWindow
from PyQt5 import QtWidgets
import sys




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    run = MainWindow()
    run.show()
    sys.exit(app.exec_())