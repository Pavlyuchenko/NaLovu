# For reading video files
import cv2
import json
import os
# For image to text conversion
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# Green color of successfull answer in RGB
GREEN_RGB = (177, 255, 111)

# Positions of answers in the video
ANSWER_A_POSITION = (960, 330)
ANSWER_B_POSITION = (960, 760)
ANSWER_C_POSITION = (960, 1180)
ANSWER_POSITIONS = [ANSWER_A_POSITION, ANSWER_B_POSITION, ANSWER_C_POSITION]

def is_green(rgb, threshold=30):
	"""
	Check if an RGB color is approximately green within a specified threshold.
	"""
	# Extract RGB components
	red, green, blue = rgb

	# Check if the color is approximately green
	within_red_range = (red >= GREEN_RGB[0] - threshold and red <= GREEN_RGB[0] + threshold)
	within_green_range = (green >= GREEN_RGB[1] - threshold and green <= GREEN_RGB[1] + threshold)
	within_blue_range = (blue >= GREEN_RGB[2] - threshold and blue <= GREEN_RGB[2] + threshold)	

	return within_red_range and within_green_range and within_blue_range

test = 1
def frame_to_text(image, START_POSITION, END_POSITION, count=1):
	global test
	# crop image to only contain rectangle specified by START_POSITION and END_POSITION
	rectange = image[START_POSITION[1]:END_POSITION[1], START_POSITION[0]:END_POSITION[0]]

	# save image to file
	cv2.imwrite(f"rectange_{count*test}.jpg", rectange)

	# only keep white or black pixels that are likely to be text
	for i in range(rectange.shape[0]):
		for j in range(rectange.shape[1]):
			if rectange[i][j][0] > 210 and rectange[i][j][1] > 210 and rectange[i][j][2] > 210:
				rectange[i][j] = [255, 255, 255]
			elif rectange[i][j][0] < 80 and rectange[i][j][1] < 80 and rectange[i][j][2] < 80:
				rectange[i][j] = [0, 0, 0]
			else:
				rectange[i][j] = [255, 0, 255]

	# check if rectangle contains white pixels, if so, remove all black pixels
	contains_white = False
	for i in range(rectange.shape[0]):
		for j in range(rectange.shape[1]):
			if rectange[i][j][0] == 255 and rectange[i][j][1] == 255 and rectange[i][j][2] == 255:
				contains_white = True
				break
	
	if contains_white:
		for i in range(rectange.shape[0]):
			for j in range(rectange.shape[1]):
				if rectange[i][j][0] == 0 and rectange[i][j][1] == 0 and rectange[i][j][2] == 0:
					rectange[i][j] = [255, 0, 255]

	cv2.imwrite(f"rectange_{count*test}___.jpg", rectange)
	test += 1
	

	# save image to file
	""" if count != -1:
		cv2.imwrite(f"rectange_{count}.jpg", rectange) """

	# perform OCR on question
	question_text = pytesseract.image_to_string(rectange, lang='ces').replace("\n", " ").rstrip()

	return question_text

def perform_ocr(image, count, correct_answer):
	"""
	Performs OCR using pytesseract
	"""

	# rectangle positions of question and answers
	START_QUESTION_POSITION = (330, 820)
	END_QUESTION_POSITION = (1594, 933)
	START_ANSWER_A_POSITION = (370, 960)
	END_ANSWER_A_POSITION = (750, 1010)
	START_ANSWER_B_POSITION = (800, 960)
	END_ANSWER_B_POSITION = (1170, 1010)
	START_ANSWER_C_POSITION = (1220, 960)
	END_ANSWER_C_POSITION = (1590, 1010)

	question_text = frame_to_text(image, START_QUESTION_POSITION, END_QUESTION_POSITION)
	answer_a_text = frame_to_text(image, START_ANSWER_A_POSITION, END_ANSWER_A_POSITION)
	answer_b_text = frame_to_text(image, START_ANSWER_B_POSITION, END_ANSWER_B_POSITION)
	answer_c_text = frame_to_text(image, START_ANSWER_C_POSITION, END_ANSWER_C_POSITION)

	return {
		'question': question_text,
		'answer_a': answer_a_text,
		'answer_b': answer_b_text,
		'answer_c': answer_c_text,
		'correct_answer': correct_answer
	}

def convert_video_to_text(path):
	vidcap = cv2.VideoCapture(path)

	# get framerate
	fps = vidcap.get(cv2.CAP_PROP_FPS)

	# start at 4 minutes
	count = 4*60*fps

	vidcap.set(cv2.CAP_PROP_POS_FRAMES, count)
	success,image = vidcap.read()

	questions = []
	answer_text = {}
	while success:
		for answer_index in range(len(ANSWER_POSITIONS)):
			if is_green(image[ANSWER_POSITIONS[answer_index]]):
				answer_text = perform_ocr(image, count, answer_index)
				print(answer_text)
				# skip 15 seconds
				count += 15*fps
				vidcap.set(cv2.CAP_PROP_POS_FRAMES, count)
		if answer_text:
			questions.append(answer_text)
			answer_text = {}

		success,image = vidcap.read()

		# skip 2 seconds
		count += 2*fps
		vidcap.set(cv2.CAP_PROP_POS_FRAMES, count)
    
	# load previous questions
	with open('questions.json', 'r', encoding='utf-8') as f:
		if os.stat('questions.json').st_size == 0:
			previous_questions = []
		else:
			previous_questions = json.load(f)

	# add new questions to previous questions
	previous_questions.extend(questions)
	# save questions to file as json
	with open('questions.json', 'w', encoding='utf-8') as f:
		json.dump(previous_questions, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
	path = "/home/pavlyuchenko/Desktop/NaLovu/epizody/"
    
	for file in os.listdir(path):
		convert_video_to_text(path + file)


