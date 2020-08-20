from docx import Document
from google.cloud import vision
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os, io, sys

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"/Users/amanda/Documents/apikey.json"
client = vision.ImageAnnotatorClient()

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Recipe Scanner'
        self.x, self.y, self.w, self.h = 400, 300, 500, 300
        self.doc = Document()
        self.name = 'unnamed document.docx'
        self.selectedFiles = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.x, self.y, self.w, self.h)

        self.l1 = QLabel('Add the document\'s name below', self)
        self.l1.move(170,5)
        self.l1.resize(300,30)

        self.l2 = QLabel('If you want to add a picture of the recipe click the button below', self)
        self.l2.move(70, 70)
        self.l2.resize(500, 30)

        self.l3 = QLabel('Press the below button to select a recipe file',self)
        self.l3.move(140,125)
        self.l3.resize(500,30)

        self.l4 = QLabel('You can select multiple files at a time or after already selecting files',self)
        self.l4.move(50, 145)
        self.l4.resize(500, 30)

        self.l5 = QLabel('click the button again to add the new files onto the end of your document',self)
        self.l5.move(40, 165)
        self.l5.resize(500, 30)

        self.l6 = QLabel('',self)
        self.l6.move(250,230)
        self.l6.resize(500,30)

        self.pic = QLabel('',self)
        self.pic.resize(100, 100)
        self.pic.move(320, 60)

        self.t1 = QLineEdit(self)
        self.t1.move(200,35)
        self.t1.resize(120,20)

        self.b1 = QPushButton('Add Picture',self)
        self.b1.setFont(QFont('Arial', 15))
        self.b1.move(200, 100)
        self.b1.resize(120, 30)
        self.b1.clicked.connect(self.getPic)

        self.b2 = QPushButton('Get Recipes',self)
        self.b2.setFont(QFont('Arial', 15))
        self.b2.move(200,200)
        self.b2.resize(120,30)
        self.b2.clicked.connect(self.getRecipes)

        self.b3 = QPushButton('Done!',self)
        self.b3.setFont(QFont('Arial', 15))
        self.b3.move(220, 260)
        self.b3.resize(70, 30)
        self.b3.clicked.connect(self.close)

        self.show()

    def getPic(self):
        if self.t1.text() != '':
            self.name = self.t1.text() + '.docx'
        self.doc.save(self.name)
        dialog = QFileDialog.getOpenFileName(self, "Get Pictures", "", "Image Files (*.png *.jpg *.bmp)")
        self.doc.add_picture(dialog[0])
        pixmap = QPixmap(dialog[0])
        pixmap = pixmap.scaled(25, 25, Qt.KeepAspectRatio)
        self.pic.setPixmap(pixmap)


    def getRecipes(self):
        if self.t1.text() != '':
            self.name = self.t1.text() + '.docx'
        self.doc.save(self.name)
        dialog = QFileDialog.getOpenFileNames(self,"Get Recipes", "", "Image Files (*.png *.jpg *.bmp)")
        for i in dialog[0]:
            self.addTxt(i)
            file = i.split('/')
            self.selectedFiles.append(file[-1])
            self.l6.move(self.l6.x()-50,230)
        self.l6.setText('Selected Files: ' + ', '.join(self.selectedFiles))

    def addTxt(self, fileName):
        with io.open(fileName, 'rb') as image_file:
            content = image_file.read()

        image = vision.types.Image(content=content)

        response = client.text_detection(image=image)

        for text in response.text_annotations:
            self.doc.add_paragraph(text.description)
            break
        self.doc.save(self.name)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())