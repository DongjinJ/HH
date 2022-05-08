import sys
import BBTAutoFunction
from PyQt5.QtWidgets import *


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

        # Filter Line Edit #
        self.filterLineEdit = QLineEdit(self)
        self.filterLineEdit.setGeometry(670, 50, 200, 30)

        # Filter Push Button #
        self.filterPushButton = QPushButton('Browse', self)
        self.filterPushButton.setGeometry(880, 50, 100, 30)

        # Calculation Push Button #
        self.calculationPushButton = QPushButton('Pin 기준 저항 계산', self)
        self.calculationPushButton.setGeometry(670, 110, 200, 140)

        # Vendor Label #
        self.vendorLabel = QLabel('Vendor', self)
        self.vendorLabel.move(890, 110)

        # Vendor Combo Box #
        self.vendorComboBox = QComboBox(self)
        self.vendorComboBox.setGeometry(890, 130, 100, 30)
        self.vendorComboBox.addItem('sec')

        # Log Text Browser#
        self.logTextBrowser = QTextBrowser(self)
        self.logTextBrowser.setGeometry(20, 270, 960, 250)
        self.logTextBrowser.append('-- BBT Auto Version 1.0 --')

        self.setWindowTitle('BBTAuto v1.0')
        self.move(300, 300)
        self.resize(1000, 540)
        self.show()

    def sampleFileOpen(self):
        fileDir = ''
        fileDir = QFileDialog.getExistingDirectory(self, 'Select Sample Folder')

        if fileDir != '':
            self.sampleLineEdit.setText(fileDir)
            BBTAutoFunction.scanCSVFile(fileDir)

    def targetFileOpen(self):
        fileDir = ''
        fileDir = QFileDialog.getExistingDirectory(self, 'Select Target Folder')

        if fileDir != '':
            self.targetLineEdit.setText(fileDir)

    def mergeFileOpen(self):
        fileDir = ''
        fileDir = QFileDialog.getExistingDirectory(self, 'Select Merge Folder')

        if fileDir != '':
            self.mergeLineEdit.setText(fileDir)



if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = BBTAuto()
   sys.exit(app.exec_())