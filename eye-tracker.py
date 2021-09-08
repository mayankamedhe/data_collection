import tobii_research as tr
from datetime import *
import time, csv, sys


datafile_name = "C:/Users/Mayanka/Documents/data collection/gaze_data/" + sys.argv[1] + ".csv"

found_eyetrackers = tr.find_all_eyetrackers()
# print(found_eyetrackers)
my_eyetracker = found_eyetrackers[0]
print("Address:" + my_eyetracker.address)
print("Model: " + my_eyetracker.model)
print("Name (It's OK if this is empty): " + my_eyetracker.device_name)
print("Serial number: " + my_eyetracker.serial_number)

def gaze_data_callback(gaze_data):
	# Print gaze points of left and right eye
	print("Left eye: ({gaze_left_eye}) \t Right eye: ({gaze_right_eye})".format(
		gaze_left_eye=gaze_data['left_gaze_point_on_display_area'],
		gaze_right_eye=gaze_data['right_gaze_point_on_display_area']))

	field_names = ['Timestamp', 'left gaze', 'right gaze']
	row = [{'Timestamp' :datetime.now().strftime("%H:%M:%S.%f")[:-3] ,'left gaze' : gaze_data['left_gaze_point_on_display_area'], 'right gaze' : gaze_data['right_gaze_point_on_display_area']}]

	print("OUT1")
	with open(datafile_name, 'a', encoding='UTF8', newline='') as f_object:
		print("innnnnnnn")
		dictwriter_object = csv.DictWriter(f_object, fieldnames=field_names)
		dictwriter_object.writeheader()
		dictwriter_object.writerows(row)

		# f_object.close()
	print("OUT22222222222222222222")
my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)

time.sleep(6)

my_eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)

