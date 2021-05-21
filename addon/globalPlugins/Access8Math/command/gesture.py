import os

from python.csv import DictReader
from keyboardHandler import KeyboardInputGesture

EMPTY = set()
CTRL = set(((17, False),))
SHIFT = set(((16, False),))

def text2gestures(text):
	gestures = []
	for t in text:
		try:
			gestures.append(genGesture[t])
		except KeyError as e:
			pass
	return gestures

def load():
	BASE_DIR = os.path.dirname(__file__)
	path = os.path.join(BASE_DIR, 'gestures.csv')
	genGesture = {}
	with open(path, 'r', encoding='utf-8') as src_file:
		src_dict_csv = DictReader(src_file)
		for row in src_dict_csv:
			char = row.pop('char')
			shift = True if row.pop('shift') == "True" else False
			vkCode = int(row.pop('vkCode'))
			scanCode = int(row.pop('scanCode'))
			isExtended = True if row.pop('isExtended') == "True" else False
			if shift:
				genGesture[char] = KeyboardInputGesture(modifiers=SHIFT, vkCode=vkCode, scanCode=scanCode, isExtended=isExtended)
			else:
				genGesture[char] = KeyboardInputGesture(modifiers=EMPTY, vkCode=vkCode, scanCode=scanCode, isExtended=isExtended)

	return genGesture

genGesture = load()
