import cv2
import serial
import sys
import glob
import qt.design
import qt.port
import pyzbar.pyzbar as pyzbar
import os
from dotenv import load_dotenv
load_dotenv()
from PyQt5.QtWidgets import QWidget, QLabel, QApplication
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
import PyQt5.QtCore
from PyQt5.QtGui import QImage, QPixmap
import serial.tools.list_ports

font = cv2.FONT_HERSHEY_SIMPLEX
speeds = ['1200','2400', '4800', '9600', '19200', '38400', '57600', '115200']



class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    teamID = int(os.getenv('teamID'))
    robotID = int(os.getenv('robotID'))
    def __init__(self, port, parent=None):
        super().__init__(parent)
        try:
            ser = serial.Serial(port, int(9600))
        except Exception:
            ser = None
        self.ser = ser

    def run(self):
        cap = cv2.VideoCapture(0)
        x2, y2 = cap.get(3) // 2, cap.get(4) // 2
        while True:
            ret, frame = cap.read()

            decodedObjects = pyzbar.decode(frame)
            for obj in decodedObjects:
                x, y, w, h = obj.rect
                x1, y1 = x, y
                robotID = obj.data.split(b',')[0]
                teamID = int(obj.data.split(b',')[1]) 
                
                color = (0, 255, 0)
                if teamID != self.teamID: color = (0, 0, 255)
                if teamID == self.teamID: color = (255, 0, 0)    
                if self.ser != None:
                    if x1 < x2: self.parent().left()
                    if x1 > x2: self.parent().right()
                    if y1 > y2: self.parent().up()
                    if y1 < y2: self.parent().down()
                    if x1 == x2 and y1 == y2: self.parent().shoot()
                else:
                    if x1 < x2: print("left")
                    if x1 > x2: print("right")
                    if y1 > y2: print("up")
                    if y1 < y2: print("down")
                    if x1 == x2 and y1 == y2: print("shoot")
                team2Msg = "None"
                if teamID != self.teamID: team2Msg = "Enemy"
                if teamID == self.teamID: team2Msg = "Confe"
                robotIDMsg = "Robot: " + str(int(robotID))
                teamMsg = "Team: " + str(teamID)
                cv2.putText(frame, team2Msg, (x, y - 100), font, 1.5, (255, 0, 0))
                cv2.putText(frame, robotIDMsg, (x, y - 50), font, 1.5, (255, 0, 0))
                cv2.putText(frame, teamMsg, (x, y), font, 1.5, (255, 0, 0))
                cv2.rectangle(frame, (x, y), (x + w, y + h), color)


            key = cv2.waitKey(1)
            if key == 27:
                break
                
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

class App(QtWidgets.QMainWindow, qt.design.Ui_MainWindow):
    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def __init__(self, port, parent=None):
        super().__init__(parent, QtCore.Qt.Window)
        self.setupUi(self)
        self.th = Thread(port, self)
        self.th.changePixmap.connect(self.setImage)
        self.th.start()
        self.pushButton.clicked.connect(self.shoot)
        self.pushButton_2.clicked.connect(self.up)
        self.pushButton_3.clicked.connect(self.down)
        self.pushButton_4.clicked.connect(self.left)
        self.pushButton_5.clicked.connect(self.right)

    def shoot(self):
        self.th.ser.write(b'p')

    def down(self):
        for _ in range(int(self.lineEdit.text())):
            self.th.ser.write(b'd')

    def up(self):
        for _ in range(int(self.lineEdit.text())):
            self.th.ser.write(b'u')

    def left(self):
        for _ in range(int(self.lineEdit.text())):
            self.th.ser.write(b'l')

    def right(self):
        for _ in range(int(self.lineEdit.text())):
            self.th.ser.write(b'r')


class SelectPortWindow(QtWidgets.QMainWindow, qt.port.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        ports = []
        [ports.append(i.device) for i in list(serial.tools.list_ports.comports())]
        self.comboBox.addItems(ports)
        self.pushButton.clicked.connect(self.open)

    def open(self):
        self.hide()
        App(port=self.comboBox.currentText(), parent=self).show()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SelectPortWindow()
    ex.show()
    sys.exit(app.exec_())

cv2.waitKey(0)
cv2.destroyAllWindows()