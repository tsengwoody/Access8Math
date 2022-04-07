import json
import os
import re
import shutil

import config

from jinja2 import Environment, FileSystemLoader

PATH = os.path.dirname(os.path.dirname(__file__))
TEMPLATES_PATH = os.path.join(PATH, 'web', 'templates')
env = Environment(
	loader=FileSystemLoader(TEMPLATES_PATH),
	variable_start_string='{|{',
	variable_end_string='}|}'
)

def raw2review(data_folder, entry_file, review_folder):
	template_folder = os.path.join(PATH, 'web', 'templates')

	rawIntoReview(data_folder, review_folder)

	try:
		name, ext = entry_file.split('.')
	except:
		name = 'index'
		ext = 'txt'

	entry_html = "{}.html".format(name)
	shutil.copytree(os.path.join(template_folder, 'modules'), os.path.join(review_folder, 'modules'))
	metadata = {
		"entry": entry_html
	}
	dst = os.path.join(review_folder, 'Access8Math.json')
	with open(dst, 'w', encoding='utf8') as f:
		json.dump(metadata, f)

	for dirPath, dirNames, fileNames in os.walk(review_folder):
		for item in fileNames:
			item = os.path.join(dirPath, item)
			try:
				name = os.path.basename(item).split('.')[0]
				extend = os.path.basename(item).split('.')[1]
			except:
				name = ''
				extend = ''
			if os.path.isfile(item) and extend == 'txt':
				with open(item, "r", encoding="utf8") as f:
					text = f.read()
				html_file = text2template(text, os.path.join(os.path.dirname(item), '{}.html'.format(name)))

def rawIntoReview(data_folder, review_folder):
	try:
		shutil.rmtree(review_folder)
	except:
		pass
	shutil.copytree(data_folder, review_folder)

def text2template(value, output):
	try:
		title = os.path.basename(output).split('.')[0]
	except:
		title = 'Access8Math'
	backslash_pattern = re.compile(r"\\")
	data = backslash_pattern.sub(lambda m: m.group(0).replace('\\', '\\\\'), value)
	data = data.replace(r'`', r'\`')
	raw = data
	template = env.get_template("index.template")
	content = template.render({
		'title': title,
		'data': data,
		'raw': raw,
		'LaTeX_delimiter': config.conf["Access8Math"]["settings"]["LaTeX_delimiter"],
		'document_display': config.conf["Access8Math"]["settings"]["HTML_document_display"],
		'display': config.conf["Access8Math"]["settings"]["HTML_math_display"],
	})
	with open(output, "w", encoding="utf8", newline="") as f:
		f.write(content)
	return output
