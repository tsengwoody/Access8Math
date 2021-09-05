from functools import wraps
import html
import re
import sys

from latex2mathml import converter

def latex2mathml(latex):
	mathml = converter.convert(latex)
	mathml = html.unescape(mathml)
	return mathml

translate_dict = {
	ord("$"): r"\$",
	ord("("): r"\(",
	ord(")"): r"\)",
	ord("\\"): r"\\",
}

def textmath2laObjEdit(LaTeX_delimiter):
	def wrapper(input):
		restring = r"{delimiter_start}.*?{delimiter_end}".format(
			delimiter_start=LaTeX_delimiter["start"].translate(translate_dict),
			delimiter_end=LaTeX_delimiter["end"].translate(translate_dict),
		)
		reTexMath = re.compile(restring)
		delimiter_start_length = len(LaTeX_delimiter["start"])
		delimiter_end_length = len(LaTeX_delimiter["end"])

		point = []
		maths = reTexMath.finditer(input)
		previous = None
		index = 0
		for index, item in enumerate(maths):
			if not previous:
				start = 0
				end = item.start(0)
			else:
				start = previous.end(0)
				end = item.start(0)

			if start != end:
				point.append({
					"start": start,
					"end": end,
					"type": "text",
					"data": input[start:end],
					"index": index,
				})

			start = item.start(0)
			end = item.end(0)
			point.append({
				"start": start,
				"end": end,
				"type": "math",
				"data": input[start:end],
				"index": index,
			})
			previous = item

		start = previous.end(0) if previous else 0
		end = len(input)
		point.append({
			"start": start,
			"end": end,
			"type": "text",
			"data": input[start:end],
			"index": index+1 if previous else 0,
		})

		return point
	return wrapper

def textmath2laObj(LaTeX_delimiter):
	def wrapper(input):
		backslash_pattern = re.compile(r"\\[^`]")
		restring = r"{delimiter_start}.*?{delimiter_end}".format(
			delimiter_start=LaTeX_delimiter["start"].translate(translate_dict),
			delimiter_end=LaTeX_delimiter["end"].translate(translate_dict),
		)
		reTexMath = re.compile(restring)
		delimiter_start_length = len(LaTeX_delimiter["start"])
		delimiter_end_length = len(LaTeX_delimiter["end"])
		text = reTexMath.split(input)
		math = reTexMath.findall(input)
		length = len(math)
		datas = []

		for i in range(length):
			raw = text[i].replace('\r\n', '\n').strip('\n')
			raw = backslash_pattern.sub(lambda m:m.group(0).replace('\\', '\\\\'), raw)
			if raw != '':
				datas.append({
					'type': 'text-content',
					'data': raw,
				})
			raw = math[i][delimiter_start_length: len(math[i])-delimiter_end_length]
			raw = backslash_pattern.sub(lambda m:m.group(0).replace('\\', '\\\\'), raw)
			datas.append({
				'type': 'latex-content',
				'data': raw,
			})

		raw = text[length].replace('\n', '').strip('\n')
		raw = backslash_pattern.sub(lambda m:m.group(0).replace('\\', '\\\\'), raw)
		if raw != '':
			datas.append({
				'type': 'text-content',
					'data': raw,
			})

		return datas
	return wrapper

def laObj2mathObj(input):
	result = []
	for item in input:
		if item['type'] == 'latex-content':
			result.append({
				'type': 'math-content',
				'data': latex2mathml(item['data']),
			})
		else:
			result.append({
				'type': item['type'],
				'data': item['data'],
			})

	return result

def obj2html(data):
	content = ''
	result = ''
	htmls = []
	for item in data:
		result = ''
		if item['type'] == 'text-content':
			temp = ''
			for index, line in enumerate(item['data'].split("\n")):
				if index != 0:
					temp += '<br />'
				temp += '{}'.format(line)
			result = '{}'.format(temp)
			content += result
			htmls.append(result)
		elif item['type'] == 'math-content':
			result = '<div>{}</div>'.format(item['data'])
			content += result
			htmls.append(result)

	return {
		"content": content,
		"htmls": htmls,
	}
