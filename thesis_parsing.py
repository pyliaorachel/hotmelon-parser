import re

class SplitterConst:
	CHAPTER = '\\chapter'
	SECTION = '\\section'
	SUBSECTION = '\\subsection'
	SUBSUBSECTION = '\\subsubsection'

class RegPatternConst:
	THESIS_TITLE = r'\\title(\[.*\])?{(?P<title>.*)}'
	FIRST_PAREN = r'^(\[.*\])?{(?P<content>.*)}'
	INNER_COMMANDS = r'\\[^{}]+(\[.*\])?{[^{}]*}{(?P<content>[^{}]*)}'

class Splitter:
	def split_chapters(text):
		return text.split(SplitterConst.CHAPTER)[1:]

	def split_sections(chapter):
		return chapter.split(SplitterConst.SECTION)[1:]

	def split_subsections(section):
		return section.split(SplitterConst.SUBSECTION)[1:]

	def split_subsubsections(section):
		return section.split(SplitterConst.SUBSUBSECTION)[1:]

class Extracter:
	def remove_inner_commands(text):
		inner_cmd = re.search(RegPatternConst.INNER_COMMANDS, text)
		while inner_cmd:
			txt = inner_cmd.group(0)
			content = inner_cmd.group('content')
			text = text.replace(txt, content, 1)

			inner_cmd = re.search(RegPatternConst.INNER_COMMANDS, text)

		return text

	def extract_title(text):
		"""{title} at the first line"""
		match = re.search(RegPatternConst.FIRST_PAREN, text)
		return Extracter.remove_inner_commands(match.group('content')) if match else None

	def extract_thesis_title(text):
		"""\title{title} anywhere in text"""
		match = re.search(RegPatternConst.THESIS_TITLE, text)
		return Extracter.remove_inner_commands(match.group('title')) if match else None

class Thesis(dict):
	def __init__(self, title='', subtitle='', abstraction='', conclusion='', date=''):
		self['title'] = title
		self['subtitle'] = subtitle
		self['chapters'] = []
		self['author'] = []
		self['abstraction'] = abstraction
		self['conclusion'] = conclusion
		self['date'] = date
		self['reference'] = None

class Chapter(dict):
	def __init__(self, title=''):
		self['title'] = title
		self['sections'] = []

class Section(dict):
	def __init__(self, title=''):
		self['title'] = title
		self['keywords'] = []
		self['subsections'] = []
		self['figures'] = []
		self['tables'] = []







