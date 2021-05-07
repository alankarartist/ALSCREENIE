from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import *
import datetime
import cv2 
import numpy as np
from dateutil.relativedelta import relativedelta
from PIL import ImageGrab
from UI.AlScreenieUI import Ui_Form
from AlGUILoop.AlGUILoop import AlGUILoop, stopLoop
import sys
import os

cwd = os.path.dirname(os.path.realpath(__file__))

class MoveWidget(QtWidgets.QWidget):
    def __init__(self):
        super(MoveWidget, self).__init__()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()

class AlScreenie(MoveWidget, Ui_Form):
    def __init__(self):
        super(AlScreenie, self).__init__()
        self.setWindowIcon(QIcon(os.path.join(cwd+'\\UI\\icons', 'alscreenie.png')))
        self.setupUi(self)
        self.setGeometry(1650,200,250,50)
        sizeObject = QtWidgets.QDesktopWidget().screenGeometry(-1)
        self.W = sizeObject.width()
        self.H = sizeObject.height()
        self.pushButton.clicked.connect(self.start)
        self.pushButton_2.clicked.connect(self.stop)
        self.pushButton_3.clicked.connect(self.exitRecorder)
        self.start()
    
    @AlGUILoop   
    def record(self):
        timeStamp = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        fileName = f'Screen Recording {timeStamp}.mp4'
        filePath = os.path.join(cwd+'\\AlScreenie', fileName)
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        capturedVideo = cv2.VideoWriter(filePath, fourcc, 20.0, (self.W, self.H))
        while(True):
            frame = ImageGrab.grab(bbox=(0,0,self.W,self.H))
            frame = np.array(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.label.setText('RECORDING')
            capturedVideo.write(frame)
            yield 0.001
        
    def start(self):
        self.generator = self.record()

    def stop(self):
        stopLoop(self.generator)
        self.label.setText('')
        cv2.destroyAllWindows()

    def exitRecorder(self):
        self.stop()
        sys.exit()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    form = AlScreenie()
    form.show()
    sys.exit(app.exec_())