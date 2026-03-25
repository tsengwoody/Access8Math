# coding=utf-8

import sys


COMMAND_GESTURES = [
	("kb:alt+b", "batch"),
	("kb:alt+h", "view_math"),
	("kb:alt+i", "interact"),
	("kb:alt+upArrow", "autocomplete"),
	("kb:alt+l", "latex_command"),
	("kb:alt+m", "mark"),
	("kb:alt+t", "translate"),
]

NAVIGATE_GESTURES = [
	("kb:alt+downArrow", "navigate"),
	("kb:alt+leftArrow", "navigate"),
	("kb:alt+rightArrow", "navigate"),
	("kb:alt+shift+downArrow", "navigate"),
	("kb:alt+shift+leftArrow", "navigate"),
	("kb:alt+shift+rightArrow", "navigate"),
	("kb:alt+home", "navigate"),
	("kb:alt+end", "navigate"),
]

SHORTCUT_GESTURES = [
	("kb:f{}".format(i), "shortcut") for i in range(1, 13)
] + [
	("kb:shift+f{}".format(i), "shortcut_help") for i in range(1, 13)
] + [
	("kb:{}".format(i), "shortcut") for i in "abcdefghijklmnopqrstuvwxyz"
] + [
	("kb:shift+{}".format(i), "shortcut_help") for i in "abcdefghijklmnopqrstuvwxyz"
]

GREEK_GESTURES = [
	("kb:{}".format(i), "GreekAlphabet") for i in "abcdefghijklmnopqrstuvwxyz"
]

WRITE_NAV_KEYS = [
	c for c in "abcdefghijklmnopqrstuvwxyz1234567890`-=[];',./\\"
] + [
	"upArrow", "downArrow", "leftarrow", "rightarrow", "home", "end", "pageUp", "pageDown", "space", "enter", "delete", "backspace", "tab"
] + [
	"control+c", "control+v", "control+x", "control+t",
] + [
	"numLockNumpad{number}".format(number=i) for i in range(10)
] + [
	"numpadPlus", "numpadMinus", "numpadMultiply", "numpadDivide", "numpadEnter", "numpadDecimal"
] + [
	"numLockNumpadPlus", "numLockNumpadMinus", "numLockNumpadMultiply", "numLockNumpadDivide", "numpadDelete"
]

WRITE_NAV_GESTURES = [
	("kb:{}".format(key), "writeNav") for key in WRITE_NAV_KEYS
] + [
	("kb:shift+{}".format(key), "writeNav") for key in WRITE_NAV_KEYS
]


class WriterGestureMixin:
	def _bind_script_gestures(self, gestures):
		for key, script_name in gestures:
			self.bindGesture(key, script_name)

	def _unbind_script_gestures(self, gestures):
		import inputCore

		for key, _script_name in gestures:
			try:
				self.removeGestureBinding(key)
			except (BaseException, KeyError):
				pass
			normalized = inputCore.normalizeGestureIdentifier(key)
			if normalized in self._originGestureMap:
				self._gestureMap[normalized] = self._originGestureMap[normalized]

	def bindCommandGestures(self):
		self._bind_script_gestures(COMMAND_GESTURES)

	def unbindCommandGestures(self):
		self._unbind_script_gestures(COMMAND_GESTURES)

	def bindNavigateGestures(self):
		self._bind_script_gestures(NAVIGATE_GESTURES)

	def unbindNavigateGestures(self):
		self._unbind_script_gestures(NAVIGATE_GESTURES)

	def bindShortcutGestures(self):
		self._bind_script_gestures(SHORTCUT_GESTURES)

	def unbindShortcutGestures(self):
		self._unbind_script_gestures(SHORTCUT_GESTURES)

	def bindGreekAlphabetGestures(self):
		self._bind_script_gestures(GREEK_GESTURES)

	def unbindGreekAlphabetGestures(self):
		self._unbind_script_gestures(GREEK_GESTURES)

	def bindWriteNavGestures(self):
		self._bind_script_gestures(WRITE_NAV_GESTURES)

	def unbindWriteNavGestures(self):
		self._unbind_script_gestures(WRITE_NAV_GESTURES)

	def gesture_not_concurrent(self):
		writer_module = sys.modules[__package__]
		if writer_module.shortcut_mode:
			writer_module.shortcut_mode = not writer_module.shortcut_mode
			self.unbindShortcutGestures()
		if writer_module.greekAlphabet_mode:
			writer_module.greekAlphabet_mode = not writer_module.greekAlphabet_mode
			self.unbindGreekAlphabetGestures()
