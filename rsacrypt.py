from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time, sys, traceback, random, re, os
import tkinter
from tkinter import filedialog
import sys, re, os
import random
from random import randint
from PIL import Image

from rsa_generator import RSAgenerator

root = tkinter.Tk()
root.withdraw()

class Validator(QValidator):
    def validate(self, string, pos):
        special = False
        regex = re.compile("^[a-zA-Z0-9 ]*$")
        if(regex.match(string)):
            special = True
        if(special):
            return QValidator.Acceptable, string, pos
        else:
            return QValidator.Invalid, string, pos

class Okno(QMainWindow):
    def __init__(self,*args,**kwargs):
        self.textregex = re.compile("^.*\.txt$")

        super(Okno, self).__init__(*args,*kwargs)
        self.setWindowTitle("RSA Cryptography")

        titleText = QLabel()
        titleText.setText("RSA Cryptography")
        titleText.setAlignment(Qt.AlignHCenter)
        titleText.setFont(QFont('times',40))
        titleText.setStyleSheet("QLabel { color : rgb(10,50,60); }")

        emptyLine = QLabel()
        emptyLine.setText("")
        emptyLine.setFont(QFont('times',20))

        authorText = QLabel()
        authorText.setText("Karol Sienkiewicz 140774")
        authorText.setAlignment(Qt.AlignHCenter)
        authorText.setFont(QFont('times',10))
        authorText.setStyleSheet("QLabel { color : rgb(10,50,60); }")

        self.fileName = QLineEdit()
        self.validator = Validator()
        self.fileName.setValidator(self.validator)
        self.fileName.setPlaceholderText("Nazwa pliku do zapisu")

        self.timeText = QLabel()
        self.timeText.setText("")
        self.timeText.setAlignment(Qt.AlignHCenter)
        self.timeText.setFont(QFont('times',12))
        self.timeText.setStyleSheet("QLabel { color : rgb(10,50,60); }")

        selectTextButton = QPushButton()
        selectTextButton.setText("Zaszyfruj")
        selectTextButton.setMinimumWidth(150)
        selectTextButton.clicked.connect(self.selectTextClicked)

        selectKeyButton = QPushButton()
        selectKeyButton.setText("Odszyfruj")
        selectKeyButton.setMinimumWidth(150)
        selectKeyButton.clicked.connect(self.selectKeyClicked)

        selectLayout = QHBoxLayout()
        selectLayout.addWidget(selectTextButton)
        selectLayout.addWidget(selectKeyButton)
        selectLayoutW = QWidget()
        selectLayoutW.setLayout(selectLayout)

        generateButton = QPushButton()
        generateButton.setText("Wygeneruj klucze")
        generateButton.setMinimumWidth(150)
        generateButton.clicked.connect(self.generateClicked)

        generateLayout = QHBoxLayout()
        generateLayout.addWidget(generateButton)
        generateLayoutW = QWidget()
        generateLayoutW.setLayout(generateLayout)

        infoButton = QPushButton()
        infoButton.setText("Informacje")
        infoButton.clicked.connect(self.infoClicked)

        helpButton = QPushButton()
        helpButton.setText("Pomoc")
        helpButton.clicked.connect(self.helpClicked)
    
        selectFinLayout = QVBoxLayout()
        selectFinLayout.setAlignment(Qt.AlignCenter)
        selectFinLayout.addWidget(selectLayoutW)
        selectFinLayoutW = QWidget()
        selectFinLayoutW.setLayout(selectFinLayout)

        topLayout = QHBoxLayout()
        topLayout.addWidget(infoButton)
        topLayout.addWidget(helpButton)
        topLayoutW = QWidget()
        topLayoutW.setLayout(topLayout)

        mainMenu = QVBoxLayout()
        mainMenu.addWidget(topLayoutW)
        mainMenu.addWidget(titleText)
        mainMenu.addWidget(emptyLine)
        mainMenu.addWidget(self.fileName)
        mainMenu.addWidget(emptyLine)
        mainMenu.addWidget(selectFinLayoutW)
        mainMenu.addWidget(generateLayoutW)
        mainMenu.addWidget(self.timeText)
        mainMenu.addWidget(authorText)

        mainMenuW = QWidget()
        mainMenuW.setLayout(mainMenu)

        self.setCentralWidget(mainMenuW)

    def loadKey(self):
        codePath = filedialog.askopenfilename()
        if(self.textregex.match(codePath)):
            with open(codePath,"r") as file:
                code = file.readline()
                code = code.replace("(","")
                code = code.replace(")","")
                code = code.replace(",","")
                code = code.split()
                return (int(code[0]),int(code[1]))
        else:
            message = QMessageBox()
            message.setWindowTitle("Błąd")
            message.setIcon(QMessageBox.Critical)
            message.setText("Wybrany pierwszy plik nie jest w odpowiednim formacie!")
            message.exec_()
            return 0

    def power(self,x, y, p):
        res = 1
        x = x % p
        while (y > 0):
            if ((y & 1) == 1):
                res = (res * x) % p
            y = y >> 1
            x = (x * x) % p
        return res

    def selectTextClicked(self):
        filePath = filedialog.askopenfilename()
        if(self.textregex.match(filePath)):
            
            code = self.loadKey()
            if(code == 0):
                message = QMessageBox()
                message.setWindowTitle("Błąd")
                message.setIcon(QMessageBox.Critical)
                message.setText("Wybrany klucz jest niepoprawny!")
                message.exec_()
                return 0

            timeStop = 0
            timeStart = time.time()
            
            with open(filePath) as file:
                text = file.read()

            char_text = [ord(letter) for letter in text]
            encrypted_text = [self.power(letter, code[0], code[1]) for letter in char_text]

            timeStop = time.time()
            self.timeText.setText("Pracę wykonano w ciągu " + str(timeStop - timeStart) + "s!")

            with open("encrypt/"+self.fileName.text()+".txt","w") as output:
                for x in encrypted_text:
                    output.write(str(x) + " ")
        else:
            message = QMessageBox()
            message.setWindowTitle("Błąd")
            message.setIcon(QMessageBox.Critical)
            message.setText("Wybrany plik nie jest w odpowiednim formacie!")
            message.exec_()

    def selectKeyClicked(self):
        filePath = filedialog.askopenfilename()
        if(self.textregex.match(filePath)):

            code = self.loadKey()
            if(code == 0):
                message = QMessageBox()
                message.setWindowTitle("Błąd")
                message.setIcon(QMessageBox.Critical)
                message.setText("Wybrany klucz jest niepoprawny!")
                message.exec_()
                return 0

            timeStop = 0
            timeStart = time.time()

            with open(filePath) as file:
                text = file.read()
            text = text.split()
            for i in range(len(text)):
                text[i] = int(text[i])
            
            pre_text = [self.power(c, code[0], code[1]) for c in text]

            for letter in pre_text:
                if not letter in range(0x110000):
                    message = QMessageBox()
                    message.setWindowTitle("Błąd")
                    message.setIcon(QMessageBox.Critical)
                    message.setText("Wybrany klucz jest niepoprawny!")
                    message.exec_()
                    return 0

            ready_text = [chr(letter) for letter in pre_text]

            timeStop = time.time()
            self.timeText.setText("Pracę wykonano w ciągu " + str(timeStop - timeStart) + "s!")

            with open("decrypt/"+self.fileName.text()+".txt","w") as output:
                for x in ready_text:
                    output.write(str(x))

        else:
            message = QMessageBox()
            message.setWindowTitle("Błąd")
            message.setIcon(QMessageBox.Critical)
            message.setText("Wybrany pierwszy plik nie jest w odpowiednim formacie!")
            message.exec_()

    def generateClicked(self):
        timeStop = 0
        timeStart = time.time()

        self.rsaGenerator = RSAgenerator()
        with open("key/"+self.fileName.text()+"_private"+".txt","w") as outputfile:
            outputfile.write(str(self.rsaGenerator.privateKey()))
        with open("key/"+self.fileName.text()+"_public"+".txt","w") as outputfile:
            outputfile.write(str(self.rsaGenerator.publicKey()))

        timeStop = time.time()
        self.timeText.setText("Pracę wykonano w ciągu " + str(timeStop - timeStart) + "s!")

    def infoClicked(self):
        with open("info.txt", "r",encoding="utf8") as f:
            infoText = f.read()
        QMessageBox.about(self, "Informacje", infoText)

    def helpClicked(self):
        with open("help.txt", "r",encoding="utf8") as f:
            helpText = f.read()
        QMessageBox.about(self, "Pomoc", helpText)
            
    

# MAIN
app = QApplication(sys.argv)

if not os.path.exists('decrypt'):
    os.makedirs('decrypt')
if not os.path.exists('encrypt'):
    os.makedirs('encrypt')
if not os.path.exists('key'):
    os.makedirs('key')

window = Okno()
window.setStyleSheet("background-color: rgb(230,235,235);")
window.setFixedWidth(600)
window.show()

app.exec_()