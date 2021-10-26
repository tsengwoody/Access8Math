import os
from languageHandler import getLanguageDescription


def getAvailableLanguages(path, category="speech"):
	"""generates a list of locale names, plus their full localized language and country names.
	@rtype: list of tuples
	"""
	# Make a list of all the locales found in NVDA's locale dir
	languages = [x for x in os.listdir(os.path.join(path, 'locale', category)) if not x.startswith('.')]
	languages = [x for x in languages if os.path.isfile(os.path.join(path, 'locale', category, x, 'unicode.dic'))]
	languages = [x for x in languages if os.path.isfile(os.path.join(path, 'locale', category, x, 'math.rule'))]
	# Make sure that en (english) is in the list as it may not have any locale files, but is default
	if 'en' not in languages:
		languages.append('en')
		languages.sort()
	# For each locale, ask Windows for its human readable display name
	descriptions = []
	for i in languages:
		desc = getLanguageDescription(i)
		label = "%s, %s" % (desc, i) if desc else i
		descriptions.append(label)
	# include a 'user default, windows' language, which just represents the default language for this user account
	languages.append("Windows")
	# Translators: the label for the Windows default NVDA interface language.
	descriptions.append(_("User default"))
	# return a zipped up version of both the lists (a list with tuples of locale,label)
	return list(zip(languages, descriptions))
