from PyQt5 import QtCore, QtGui, QtWidgets
import sys, os, csv 
from PyQt5.QtWidgets import * 
from datetime import *
import numpy as np
import pandas as pd
import time

# import keyboard
# from pyglet.window import *
# import cv2
# import pyautogui
# import tobii_research as tr


# global_gaze_data = None
# global_time_gaze = None
# my_eyetracker = None



# def gaze_data_callback(gaze_data):
# 	global global_gaze_data
# 	global_gaze_data = gaze_data

# 	global_time_gaze.append(datetime.now().strftime("%H:%M:%S.%f")[:-3])
# 	# Print gaze points of left and right eye
# 	gaze_left_eye=gaze_data['left_gaze_point_on_display_area']
# 	gaze_right_eye=gaze_data['right_gaze_point_on_display_area']


# 	print("Left eye: ({gaze_left_eye}) \t Right eye: ({gaze_right_eye})".format(
# 	    gaze_left_eye=gaze_left_eye,
# 	    gaze_right_eye=gaze_right_eye))

# 	field_names = ['left gaze', 'right gaze']
# 	row = {'left gaze' : gaze_left_eye, 'right gaze' : gaze_right_eye}
# 	with open('gaze_data.csv', 'a') as f_object:
# 		dictwriter_object = csv.DictWriter(f_object, fieldnames=field_names)
# 		dictwriter_object.writerow(row)

# 		f_object.close()

# found_eyetrackers = tr.find_all_eyetrackers()
# my_eyetracker = found_eyetrackers[0]
# my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)
# time.sleep(600)


###### Login Page

class MainWindow(QtWidgets.QWidget):

	switch_window = QtCore.pyqtSignal(str)

	def __init__(self):
		QtWidgets.QWidget.__init__(self)
		self.setWindowTitle('Login')

		layout = QtWidgets.QGridLayout()

		self.name = QLabel('Name')
		self.line_edit = QtWidgets.QLineEdit()
		layout.addWidget(self.name, 0, 0)
		layout.addWidget(self.line_edit, 0, 1)

		self.button = QtWidgets.QPushButton('Start')
		self.button.clicked.connect(self.switch)
		self.button.setShortcut('Return')
		layout.addWidget(self.button, 1, 1)

		self.setLayout(layout)

	def switch(self):
		self.switch_window.emit(self.line_edit.text())


class ImageLoader(QtWidgets.QWidget):

	switch_window = QtCore.pyqtSignal()
	def __init__(self, user_name):
		super().__init__()
		self.user_name = user_name

		# self.gaze_dir = "gaze/"		
		# if not os.path.exists(self.dirName):
		# 	os.makedirs(self.dirName)
		# 	print("Directory " , self.dirName ,  " Created ")
		# else:    
		# 	print("Directory " , self.dirName ,  " already exists")

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


		label = QtWidgets.QLabel(self)
		label.resize(645, 550)

		# the label alignment property is always maintained even when the contents
		# change, so there is no need to set it each time
		# self.label.setAlignment(QtCore.Qt.AlignCenter)

		dirpath = "/Users/mayankamedhe/Downloads/full code/tobiiresearch/images/"
		for f in os.listdir(dirpath):
		  fpath = os.path.join(dirpath, f)
		  if os.path.isfile(fpath) and f.endswith(('.png', '.jpg', '.jpeg')):
			  self.fileList.append(fpath)


		pixmap = QtGui.QPixmap(self.fileList[self.iterator]).scaled(label.size()) #QtCore.Qt.KeepAspectRatio
		if pixmap.isNull():
		  return
		label.setPixmap(pixmap)

		label.move(397.5,50) # wrt window

		description = QLabel('Description (Max 50 words)', self)
		description.move(397.5, 625)

		description = QLabel('Instructions:', self)
		description.move(1050, 50)
		description = QLabel('1. Describe the main objects in the image', self)
		description.move(1050, 65)
		description = QLabel('2. Can elaborate on the possible action/activity going on', self)
		description.move(1050, 80)
		description = QLabel('3. Include as many adjectives as possible for the objects', self)
		description.move(1050, 95)
		description = QLabel('4. Description can be 3-4 lines long for each image', self)
		description.move(1050, 110)

		descriptionEdit = QTextEdit(self)
		descriptionEdit.move(397.5, 650)
		descriptionEdit.resize(645, 100)
		descriptionEdit.textChanged.connect(lambda: self.save_text(descriptionEdit.toPlainText()))

		submitImageButton = QtWidgets.QPushButton('Submit (Ctrl+E)', self)
		submitImageButton.clicked.connect(lambda: self.getInfo(descriptionEdit))
		submitImageButton.setShortcut('Ctrl+E')
		submitImageButton.move(600, 800)

		nextImageButton = QtWidgets.QPushButton('Next image (Ctrl+N)',self)
		nextImageButton.move(740, 800)
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
			# image = pyautogui.screenshot()
			# image = cv2.cvtColor(np.array(image),cv2.COLOR_RGB2BGR)
			

			# img_name = self.dirName + "/image" + str(self.iterator) + "-SS"+ str(self.prev)+ ".png"
			# cv2.imwrite(img_name, image)
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

			returnValue = msg.exec()
			if returnValue == QMessageBox.Ok:
				self.iterator = 0
				a = np.array(self.global_time)
				b = np.array(self.global_array_imageName)
				c = np.array(self.global_array_text)
				df = pd.DataFrame({"Timestamp" : a, "Image Name" : b,"Text Input" : c})
				df.to_csv("CSV/"+self.user_name+".csv", index=False)
				self.switch_window.emit()
				# self.nextImage()

			# if returnValue == QMessageBox.Cancel:
				# my_eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)

	def popup_button(self, i):
		print(i.text())
			


class Controller:

	def __init__(self):
		pass

	def show_main(self):
		self.window = MainWindow()
		self.window.switch_window.connect(self.show_image)
		self.window.show()

	def show_image(self, user_name):
		self.window_image = ImageLoader(user_name)
		self.window.close()
		self.window_image.show()
		self.window_image.switch_window.connect(self.show_main)

def main():
	
	# print("Address: " + my_eyetracker.address)
	# print("Model: " + my_eyetracker.model)
	# print("Name (It's OK if this is empty): " + my_eyetracker.device_name)
	# print("Serial number: " + my_eyetracker.serial_number)


	app = QtWidgets.QApplication(sys.argv)
	controller = Controller()
	controller.show_main()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()  



