from PyQt5 import QtCore, QtGui, QtWidgets
import sys, os, csv 
from PyQt5.QtWidgets import * 
from datetime import *
import numpy as np
import pandas as pd
import tobii_research as tr
import time


# class MainWindow(QtWidgets.QWidget):

# 	switch_window = QtCore.pyqtSignal(str)

# 	def __init__(self):
# 		QtWidgets.QWidget.__init__(self)
# 		self.setWindowTitle('Login')

# 		layout = QtWidgets.QGridLayout()

# 		self.name = QLabel('Name')
# 		self.line_edit = QtWidgets.QLineEdit()
# 		layout.addWidget(self.name, 0, 0)
# 		layout.addWidget(self.line_edit, 0, 1)

# 		self.button = QtWidgets.QPushButton('Start')
# 		self.button.clicked.connect(self.switch)
# 		self.button.setShortcut('Return')
# 		layout.addWidget(self.button, 1, 1)

# 		self.setLayout(layout)

# 	def switch(self):
# 		self.switch_window.emit(self.line_edit.text())


class ImageLoader(QtWidgets.QWidget):

	switch_window = QtCore.pyqtSignal()
	def __init__(self, user_name):
		super(QtWidgets.QWidget, self).__init__()
		self.user_name = user_name

		QtWidgets.QWidget.__init__(self)
		self.fileList = []
		self.iterator = 0

		self.time = []
		self.array_text = []
		self.array_imageName = []

		self.global_time = []
		self.global_array_text = []
		self.global_array_imageName = []
		self.prev = 0

		factor_x = 2.5
		factor_y = 2.5

		label = QtWidgets.QLabel(self)
		label.resize(645*factor_x, 550*factor_y) ## (645, 800)

		# the label alignment property is always maintained even when the contents
		# change, so there is no need to set it each time
		# self.label.setAlignment(QtCore.Qt.AlignCenter)

		dirpath = "C:/Users/Mayanka/Documents/data collection/images/"
		for f in os.listdir(dirpath):
		  fpath = os.path.join(dirpath, f)
		  if os.path.isfile(fpath) and f.endswith(('.png', '.jpg', '.jpeg')):
			  self.fileList.append(fpath)


		pixmap = QtGui.QPixmap(self.fileList[self.iterator]).scaled(label.size()) #QtCore.Qt.KeepAspectRatio
		if pixmap.isNull():
		  return
		label.setPixmap(pixmap)

		label.move(397.5*factor_x,50*factor_y) # wrt window (50,50)

		description = QLabel('Description (Max 50 words)', self)
		description.move(397.5*factor_x, 625*factor_y) # (745, 50)

		description = QLabel('Instructions:', self)
		description.move(1050*factor_x, 50*factor_y)
		description = QLabel('1. Describe the main objects in the image', self)
		description.move(1050*factor_x, 65*factor_y)
		description = QLabel('2. Can elaborate on the possible action/activity going on', self)
		description.move(1050*factor_x, 80*factor_y)
		description = QLabel('3. Include as many adjectives as possible for the objects', self)
		description.move(1050*factor_x, 95*factor_y)
		description = QLabel('4. Description can be 3-4 lines long for each image', self)
		description.move(1050*factor_x, 110*factor_y)

		descriptionEdit = QTextEdit(self)
		descriptionEdit.move(397.5*factor_x, 650*factor_y) ## (745, 70)
		descriptionEdit.resize(645*factor_x, 100*factor_y) ## (645, 400)
		descriptionEdit.textChanged.connect(lambda: self.save_text(descriptionEdit.toPlainText()))

		submitImageButton = QtWidgets.QPushButton('Submit (Ctrl+E)', self)
		submitImageButton.clicked.connect(lambda: self.getInfo(descriptionEdit))
		submitImageButton.setShortcut('Ctrl+E')
		submitImageButton.move(600*factor_x, 800*factor_y) ## (900, 500)

		nextImageButton = QtWidgets.QPushButton('Next image (Ctrl+N)',self)
		nextImageButton.move(740*factor_x, 800*factor_y) ## (1100, 500)
		nextImageButton.clicked.connect(lambda: self.nextImage(label))
		nextImageButton.setShortcut('Ctrl+N')

		self.iterator += 1

		geometry = QApplication.desktop().availableGeometry()
		geometry.setHeight(geometry.height())
		print(geometry) # PyQt5.QtCore.QRect(0, 25, 1440, 818)

		self.setGeometry(geometry)
		self.show()
		

	def save_text(self, text):

		self.array_text = text.split()
		if(len(self.array_text) == self.prev + 1):
			self.time.append(datetime.now().strftime("%H:%M:%S.%f")[:-3])
			self.prev += 1
			self.array_imageName.append(self.fileList[self.iterator - 1])


	def getInfo(self, descriptionEdit):

		self.global_time += self.time
		self.global_array_imageName += self.array_imageName
		self.global_array_text += self.array_text 

		self.time = []
		self.array_imageName = []
		self.array_text = []
		self.prev = 0
		descriptionEdit.clear()
		

	def nextImage(self, label):
		try:
			filename = self.fileList[self.iterator]
			pixmap = QtGui.QPixmap(filename).scaled(label.size()) #  QtCore.Qt.KeepAspectRatio
			self.iterator += 1

			if pixmap.isNull():
				# the file is not a valid image, remove it from the list
				# and try to load the next one
				self.fileList.remove(filename)
				self.nextImage()
			else:
				label.setPixmap(pixmap)

		except:
			msg = QtWidgets.QMessageBox()
			msg.setText("Congratulations! Task Completed. Restart?")
			msg.setStandardButtons(QMessageBox.Cancel|QMessageBox.Ok)
			msg.setDefaultButton(QMessageBox.Retry)
			msg.buttonClicked.connect(self.popup_button)

			returnValue = msg.exec_()
			if returnValue == QMessageBox.Ok:
				self.iterator = 0
				a = np.array(self.global_time)
				b = np.array(self.global_array_imageName)
				c = np.array(self.global_array_text)
				df = pd.DataFrame({"Timestamp" : a, "Image Name" : b,"Text Input" : c})
				df.to_csv("text_data/"+self.user_name+".csv", index=False)
				self.switch_window.emit()
				# self.nextImage()

	def popup_button(self, i):
		print(i.text())
			


class Controller:

	def __init__(self):
		pass

	# def show_main(self):
	# 	self.window = MainWindow()
	# 	self.window.switch_window.connect(self.show_image)
	# 	self.window.show()

	def show_image(self, user_name):
		self.window_image = ImageLoader(user_name)
		# self.window.close()
		self.window_image.show()
		# self.window_image.switch_window.connect(self.show_main)

def main():
	app = QtWidgets.QApplication(sys.argv)
	controller = Controller()
	controller.show_image(sys.argv[1])
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()  
