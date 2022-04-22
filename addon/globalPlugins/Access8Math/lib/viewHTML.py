import io
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

import html5lib
import markdown2
import xml.etree.ElementTree as etree


def raw2review(data_folder, entry_file, review_folder):
	with io.open(os.path.join(data_folder, entry_file), 'r', encoding='utf8') as f:
		content = f.read()
	contentmd = markdown2.markdown(content)

	tb = html5lib.getTreeBuilder("etree", implementation=etree)
	p = html5lib.HTMLParser(tb)
	try:
		contentxml = p.parse(contentmd)
	except BaseException:
		contentxml = None

	resources = []
	if contentxml:
		for item in contentxml.iter('{http://www.w3.org/1999/xhtml}a'):
			resource = '\\'.join(item.attrib['href'].split('/'))
			resources.append(resource)
		for item in contentxml.iter('{http://www.w3.org/1999/xhtml}img'):
			resource = '\\'.join(item.attrib['src'].split('/'))
			resources.append(resource)
	print(resources)
	template_folder = os.path.join(PATH, 'web', 'templates')

	rawIntoReview(data_folder, review_folder, resources)

	shutil.copyfile(
		os.path.join(data_folder, entry_file),
		os.path.join(review_folder, entry_file),
	)
	shutil.copytree(
		os.path.join(template_folder, 'modules'),
		os.path.join(review_folder, 'modules')
	)

	try:
		name = entry_file.split('.')[0]
	except BaseException:
		name = 'index'
	entry_html = "{}.html".format(name)
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
			except BaseException:
				name = ''
				extend = ''
			if os.path.isfile(item) and extend == 'txt':
				with open(item, "r", encoding="utf8") as f:
					text = f.read()
				text2template(text, os.path.join(os.path.dirname(item), '{}.html'.format(name)))


def rawIntoReview(data_folder, review_folder, resources):
	try:
		shutil.rmtree(review_folder)
	except BaseException:
		pass
	try:
		os.mkdir(review_folder)
	except BaseException:
		pass
	for resource in resources:
		try:
			dir = os.path.dirname(os.path.join(review_folder, resource))
			if not os.path.exists(dir):
				os.mkdir(dir)
			shutil.copyfile(
				os.path.join(data_folder, resource),
				os.path.join(review_folder, resource),
			)
		except BaseException:
			pass


def text2template(value, output):
	try:
		title = os.path.basename(output).split('.')[0]
	except BaseException:
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
		'color': config.conf["Access8Math"]["settings"]["color"],
		'bg_color': config.conf["Access8Math"]["settings"]["bg_color"],
	})
	with open(output, "w", encoding="utf8", newline="") as f:
		f.write(content)
	return output
