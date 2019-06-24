from PyQt5 import QtCore, QtGui, QtWidgets
from imutils import paths
import os
import numpy as np
import argparse
import imutils
import cv2

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("ScreenStitch")
        MainWindow.resize(531, 525)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.selectFolder = QtWidgets.QPushButton(self.centralwidget)
        self.selectFolder.setGeometry(QtCore.QRect(30, 30, 211, 31))
        self.selectFolder.setObjectName("selectFolder")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(260, 30, 241, 111))
        self.listWidget.setObjectName("listWidget")
        self.stitchBtn = QtWidgets.QPushButton(self.centralwidget)
        self.stitchBtn.setGeometry(QtCore.QRect(30, 70, 211, 31))
        self.stitchBtn.setObjectName("stitchBtn")
        self.result = QtWidgets.QLabel(self.centralwidget)
        self.result.setGeometry(QtCore.QRect(30, 160, 471, 321))
        self.result.setFrameShape(QtWidgets.QFrame.Box)
        self.result.setText("")
        self.result.setObjectName("result")
        self.ClearBtn = QtWidgets.QPushButton(self.centralwidget)
        self.ClearBtn.setGeometry(QtCore.QRect(30, 110, 211, 31))
        self.ClearBtn.setObjectName("ClearBtn")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 531, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.selectFolder.clicked.connect(self.getFolder)
        self.stitchBtn.clicked.connect(self.stitchImage)
        self.ClearBtn.clicked.connect(self.clearScreen)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ScreenStitch"))
        self.selectFolder.setText(_translate("MainWindow", "Select Images"))
        self.stitchBtn.setText(_translate("MainWindow", "Generate Stitching"))
        self.ClearBtn.setText(_translate("MainWindow", "Clear"))

    def getFolder(self):
        OutputFolder, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select Images", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        self.listWidget.addItem(OutputFolder)

    def clearScreen(self):
        self.listWidget.clear()

    def stitchImage(self):
        selectedItems = []
        imagePaths = []
        for i in range(self.listWidget.count()):
            selectedItems.append(self.listWidget.item(i))
        for item in selectedItems:
            imagePaths.append(item.text())
        imagePaths = sorted(list(imagePaths))

        images = []

        for imagePath in imagePaths:
            image = cv2.imread(imagePath)
            image = imutils.rotate_bound(image, 90)
            images.append(image)

        self.listWidget.addItem("[INFO] stitching images...")
        stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()
        (status, stitched) = stitcher.stitch(images)
    
        if status == 0:
            stitched = imutils.rotate_bound(stitched, 270)
            cv2.imwrite("output.png", stitched)
            self.listWidget.addItem("[INFO] image stitching success...")
            self.listWidget.addItem("[INFO] Results are saved at screenstitch directory")

            outputDir = os.getcwd()+"\output.png"

            pixmap = QtGui.QPixmap(outputDir)
            pixmap = pixmap.scaled(self.result.width(), self.result.height(), QtCore.Qt.KeepAspectRatio)
            self.result.setPixmap(pixmap)
            self.result.setAlignment(QtCore.Qt.AlignCenter)

        elif status == 1: 
            self.listWidget.addItem("[INFO] image stitching failed: needs more images (1)")
        elif status == 2: 
            self.listWidget.addItem("[INFO] image stitching failed: not enough keypoints (2)")  
        else:
            self.listWidget.addItem("[INFO] image stitching failed: camera error (3)")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

