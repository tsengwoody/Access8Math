import os
from languageHandler import getLanguageDescription

def getAvailableLanguages(path):
	"""generates a list of locale names, plus their full localized language and country names.
	@rtype: list of tuples
	"""
	#Make a list of all the locales found in NVDA's locale dir
	l=[x for x in os.listdir(path +'/locale') if not x.startswith('.')]
	l=[x for x in l if os.path.isfile(path +'/locale/%s/unicode.dic'%x)]
	#Make sure that en (english) is in the list as it may not have any locale files, but is default
	if 'en' not in l:
		l.append('en')
		l.sort()
	#For each locale, ask Windows for its human readable display name
	d=[]
	for i in l:
		desc=getLanguageDescription(i)
		label="%s, %s"%(desc,i) if desc else i
		d.append(label)
	#include a 'user default, windows' language, which just represents the default language for this user account
	l.append("Windows")
	# Translators: the label for the Windows default NVDA interface language.
	d.append(_("User default"))
	#return a zipped up version of both the lists (a list with tuples of locale,label)
	return list(zip(l,d))
