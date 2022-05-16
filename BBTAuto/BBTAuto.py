import sys
import BBTAutoFunction
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import *
import psutil
import os

class BBTAuto(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Sample Label #
        self.sampleLabel = QLabel('샘플링 저항 경로', self)
        self.sampleLabel.move(20, 20)

        # Sample Line Edit #
        self.sampleLineEdit = QLineEdit(self)
        self.sampleLineEdit.setText('D:\\BBT\\SamplingSource\\')
        self.sampleLineEdit.setGeometry(20, 50, 500, 30)

        # Sample Push Button #
        self.samplePushButton = QPushButton('Browse', self)
        self.samplePushButton.setGeometry(540, 50, 100, 30)
        self.samplePushButton.clicked.connect(self.sampleFileOpen)

        # Target Label #
        self.targetLabel = QLabel('타겟 경로', self)
        self.targetLabel.move(20, 100)

        # Target Line Edit #
        self.targetLineEdit = QLineEdit(self)
        self.targetLineEdit.setText('D:\\BBT\\SamplingTarget\\')
        self.targetLineEdit.setGeometry(20, 130, 500, 30)

        # Target Push Button #
        self.targetPushButton = QPushButton('Browse', self)
        self.targetPushButton.setGeometry(540, 130, 100, 30)
        self.targetPushButton.clicked.connect(self.targetFileOpen)

        # Merge Label #
        self.mergeLabel = QLabel('머지 경로', self)
        self.mergeLabel.move(20, 180)

        # Merge Line Edit #
        self.mergeLineEdit = QLineEdit(self)
        self.mergeLineEdit.setText('D:\\BBT\\SamplingMerged\\')
        self.mergeLineEdit.setGeometry(20, 210, 500, 30)

        # Merge Push Button #
        self.mergePushButton = QPushButton('Browse', self)
        self.mergePushButton.setGeometry(540, 210, 100, 30)
        self.mergePushButton.clicked.connect(self.mergeFileOpen)

        # Filter Label #
        self.filterLabel = QLabel('필터용 파일명', self)
        self.filterLabel.move(670, 20)

        # Filter Combo Box #
        self.filterComboBox = QComboBox(self)
        self.filterComboBox.setGeometry(670, 50, 200, 30)

        # Filter Push Button #
        self.filterPushButton = QPushButton('Filter Set', self)
        self.filterPushButton.setGeometry(880, 50, 100, 30)
        self.filterPushButton.clicked.connect(self.filterFileSelect)

        # Calculation Push Button #
        self.calculationPushButton = QPushButton('Pin 기준 저항 계산', self)
        self.calculationPushButton.setGeometry(670, 110, 200, 140)

        # Vendor Label #
        self.vendorLabel = QLabel('Vendor', self)
        self.vendorLabel.move(890, 110)

        # Vendor Combo Box #
        self.vendorComboBox = QComboBox(self)
        self.vendorComboBox.setGeometry(890, 130, 100, 30)
        self.vendorComboBox.addItem('SEC')
        self.vendorComboBox.addItem('Hynix')

        # Memory Label #
        self.memoryLabel = QLabel('Memory', self)
        self.memoryLabel.move(890, 180)

        # Memory Progress Bar #
        self.memoryProgressBar = QProgressBar(self)
        self.memoryProgressBar.setGeometry(890, 200, 100, 20)

        # Log Text Browser #
        self.logTextBrowser = QTextBrowser(self)
        self.logTextBrowser.setGeometry(20, 270, 960, 250)
        self.logTextBrowser.append('-- BBT Auto Version 1.0 --')

        # Timer #
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.periodicTask)
        self.timer.start()

        self.setWindowTitle('BBTAuto v1.0')
        self.move(300, 300)
        self.setFixedSize(1000, 540)
        self.show()

    def periodicTask(self):
        # AFTER  code
        memory_usage_dict = dict(psutil.virtual_memory()._asdict())
        memory_usage_percent = memory_usage_dict['percent']
        self.memoryProgressBar.setValue(int(memory_usage_percent))

    def sampleFileOpen(self):
        self.fileDir = ''
        self.fileDir = QFileDialog.getExistingDirectory(self, 'Select Sample Folder')

        if self.fileDir != '':
            self.sampleLineEdit.setText(self.fileDir)
            self.logTextBrowser.append('>> Open sample Path ..')
            csvList = BBTAutoFunction.scanCSVFile(self.fileDir)
            self.logTextBrowser.append(' => Complete Find CSV File\n')
            self.logTextBrowser.append('-- CSV File List --')
            for i in csvList:
                self.logTextBrowser.append(' =>' + i)
            self.filterComboBox.addItems(csvList)

    def targetFileOpen(self):
        fileDir = ''
        fileDir = QFileDialog.getExistingDirectory(self, 'Select Target Folder')

        if fileDir != '':
            self.logTextBrowser.append('>> Open target Path ..')
            self.targetLineEdit.setText(fileDir)

    def mergeFileOpen(self):
        fileDir = ''
        fileDir = QFileDialog.getExistingDirectory(self, 'Select Merge Folder')

        if fileDir != '':
            self.mergeLineEdit.setText(fileDir)

    def filterFileSelect(self):
        filterFile = self.filterComboBox.currentText()
        targetPath = self.targetLineEdit.text()
        mergedPath = self.mergeLineEdit.text()
        vendor = self.vendorComboBox.currentText()
        self.logTextBrowser.append('>> Select CSV File: ' + filterFile)
        if os.path.isdir(self.fileDir) == True and os.path.isdir(targetPath) == True and os.path.isdir(mergedPath):
            BBTAutoFunction.scanTargetCSV(self.fileDir, filterFile, targetPath, self.logTextBrowser, vendor, mergedPath)
        else:
            self.logTextBrowser.append('! [Error]: Please Check sampleFile Path or targetFile Path')


if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = BBTAuto()
   sys.exit(app.exec_())