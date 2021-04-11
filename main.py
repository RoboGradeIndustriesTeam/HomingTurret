import cv2
import serial
import sys
import traceback
import qt.design
import qt.port
from PyQt5.QtWidgets import QWidget, QLabel, QApplication
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
import PyQt5.QtCore
from PyQt5.QtGui import QImage, QPixmap
import serial.tools.list_ports

font = cv2.FONT_HERSHEY_SIMPLEX
face_cascade = cv2.CascadeClassifier('face.xml')


class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def __init__(self, port, parent=None):
        super().__init__(parent)
        try:
            ser = serial.Serial(port, int(9600))
        except Exception:
            ser = None
        self.ser = ser

    def run(self):
        try:
            cap = cv2.VideoCapture(0)
            x2, y2 = cap.get(3) // 2, cap.get(4) // 2
            while True:
                ret, frame = cap.read()

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                img = frame
                img = cv2.circle(frame, (int(x2), int(y2)), 5, (255, 255, 255), 2)
                for (x, y, w, h) in faces:
                    x1, y1 = x, y
                    img = cv2.circle(frame, (x + w // 2, y + h // 2), 15, (255, 255, 255), 2)
                    img = cv2.putText(img, "Face: " + str((x + w // 2, y + h // 2)), (x, y), font,
                                      1, (255, 255, 255), 2, cv2.LINE_AA)

                    if int(self.parent().auto_2.checkState()) == 2:
                        if x1 < x2: self.parent().left()
                        if x1 > x2: self.parent().right()
                        if y1 > y2: self.parent().down()
                        if y1 < y2: self.parent().up()
                        if int(self.parent().fireAllow.checkState()) == 2 and (x1 - x2 < 5 and y1 - y2 < 5) or int(
                                self.parent().fireAllow.checkState()) == 2 and (
                                x1 - x2 > -5 and y1 - y2 > -5): self.parent().shoot()
                if ret:
                    rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    h, w, ch = rgbImage.shape
                    bytesPerLine = ch * w
                    convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                    p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                    self.changePixmap.emit(p)
        except Exception:
            print(traceback.format_exc())


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
        self.pushButton_2.clicked.connect(self.down)
        self.pushButton_3.clicked.connect(self.up)
        self.pushButton_4.clicked.connect(self.left)
        self.pushButton_5.clicked.connect(self.right)

    def shoot(self):
        if self.th.ser is not None:
            self.th.ser.write(b'p')
            print("[INFO] Shoot")
        else:
            print("[ACTION] Shoot")

    def up(self):
        if self.th.ser is not None:
            try:
                for _ in range(int(self.lineEdit.text())):
                    self.th.ser.write(b'u')
            except ValueError:
                self.th.ser.write(b'u')
            print("[INFO] Up")
        else:
            print("[ACTION] Up")

    def down(self):
        if self.th.ser is not None:
            try:
                for _ in range(int(self.lineEdit.text())):
                    self.th.ser.write(b'd')
            except ValueError:
                self.th.ser.write(b'd')
            print("[INFO] Down")
        else:
            print("[ACTION] Down")

    def left(self):
        if self.th.ser is not None:
            try:
                for _ in range(int(self.lineEdit.text())):
                    self.th.ser.write(b'l')
            except ValueError:
                self.th.ser.write(b'l')
            print("[INFO] Left")
        else:
            print("[ACTION] Left")

    def right(self):
        if self.th.ser is not None:
            try:
                for _ in range(int(self.lineEdit.text())):
                    self.th.ser.write(b'r')
            except ValueError:
                self.th.ser.write(b'r')
            print("[INFO] Right")
        else:
            print("[ACTION] Right")


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
