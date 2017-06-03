import re
import glob

class SplitterConst:
	CHAPTER = '\\chapter'
	SECTION = '\\_section'

class RegPatternConst:
	THESIS_TITLE = r'\\title(\[.*\])?{(?P<title>.*)}'
	FIRST_PAREN = r'^(\[.*\])?{(?P<content>.*)}'
	AUTHOR = r'\\author(\[.*\])?{(?P<author>.*)}'
	ABSTRACT = r'\\begin{abstract}\n*(?P<abstract>.*)\n*\\end{abstract}'
	DATE = r'\\degreedate(\[.*\])?{(?P<date>.*)}'
	SUBTITLE = r'\\subtitle(\[.*\])?{(?P<subtitle>.*)}'
	GRAPHIC_PATH = r'\\graphicspath{(?P<paths>.*)}'
	GRAPHIC = r'\\includegraphics(\[.*\])?{(?P<graphic>.*)}'

	INNER_COMMANDS_REPLACE = r'\\[^{}]+(\[.*\])?{[^{}]*}{(?P<content>[^{}]*)}'
	CONFIG_COMMANDS = r'\\[^ \t\n]*({.*})?'
	COMMENTS = r'\%.*\n*'
	TABLE = r'\\begin{table}\n*(?P<content>(.|\n)*)\n*\\end{table}'

class Splitter:
	def split_chapters(text):
		splitted = text.split(SplitterConst.CHAPTER)
		return splitted[1:]

	def split_sections(text, level=0):
		splitted = text.split(SplitterConst.SECTION.replace('_', 'sub' * level))
		return (splitted[0], splitted[1:])

class Extracter:
	def remove_inner_commands(text):
		# replacible inner commands
		inner_cmd = re.search(RegPatternConst.INNER_COMMANDS_REPLACE, text)
		while inner_cmd:
			txt = inner_cmd.group(0)
			content = inner_cmd.group('content')
			text = text.replace(txt, content, 1)

			inner_cmd = re.search(RegPatternConst.INNER_COMMANDS_REPLACE, text)

		# config commands
		inner_cmd = re.search(RegPatternConst.CONFIG_COMMANDS, text)
		while inner_cmd:
			text = text.replace(inner_cmd.group(0), '')
			inner_cmd = re.search(RegPatternConst.CONFIG_COMMANDS, text)

		return text

	def remove_header(text):
		return re.sub(RegPatternConst.FIRST_PAREN, '', text, 1)

	def remove_comments(text):
		return re.sub(RegPatternConst.COMMENTS, '', text)

	def remove_table(text):
		return re.sub(RegPatternConst.TABLE, '', text)

	def clean_content(text):
		text = Extracter.remove_header(text)
		text = Extracter.remove_table(text)
		text = Extracter.remove_comments(text)
		text = Extracter.remove_inner_commands(text)
		text = text.strip()
		return text

	def extract_to_list(text):
		"""{{e1}{e2}...{en}}"""
		l = text.split('{')[1:]
		l = list(map(lambda e: e[:-1], l)) # remove trailing '}'
		return l

	def extract_graphic_paths(text):
		match = re.search(RegPatternConst.GRAPHIC_PATH, text)
		return Extracter.extract_to_list(match.group('paths')) if match else None

	def extract_figures(text, path_prefix, base_path):
		match = re.finditer(RegPatternConst.GRAPHIC, text)
		figures = list(map(lambda m: m.group('graphic'), match))

		figure_paths = []
		for figure in figures:
			for path in path_prefix:
				full_path = '{}/{}{}.*'.format(base_path, path, figure)
				if glob.glob(full_path):
					f_ext = glob.glob(full_path)[0].split('.')[-1]
					figure_paths.append('{}{}.{}'.format(path, figure, f_ext))

		return figure_paths

	def extract_title(text):
		"""{title} at the first line"""
		match = re.search(RegPatternConst.FIRST_PAREN, text)
		return Extracter.remove_inner_commands(match.group('content')) if match else ''

	def extract_thesis_title(text):
		"""\title{title} anywhere in text"""
		match = re.search(RegPatternConst.THESIS_TITLE, text)
		return Extracter.remove_inner_commands(match.group('title')) if match else ''

	def extract_authors(text):
		"""\author[*]{author}"""
		match = re.finditer(RegPatternConst.AUTHOR, text)
		authors = list(map(lambda m: m.group('author'), match))
		return authors

	def extract_abstract(text):
		"""\begin{abstract}...\end{abstract}"""
		match = re.search(RegPatternConst.ABSTRACT, text)
		return Extracter.remove_inner_commands(match.group('abstract')) if match else ''

	def extract_date(text):
		"""\degreedate{date}"""
		match = re.search(RegPatternConst.DATE, text)
		return Extracter.remove_inner_commands(match.group('date')) if match else ''

	def extract_subtitle(text):
		"""\subtitle{subtitle}"""
		match = re.search(RegPatternConst.SUBTITLE, text)
		return Extracter.remove_inner_commands(match.group('subtitle')) if match else ''

class Thesis(dict):
	def __init__(self, title='', subtitle='', abstraction='', date=''):
		self['title'] = title
		self['subtitle'] = subtitle
		self['chapters'] = []
		self['authors'] = []
		self['abstract'] = abstraction
		self['date'] = date

class Chapter(dict):
	def __init__(self, title='', content=''):
		self['title'] = title
		self['sections'] = []
		self['content'] = content

class Section(dict):
	def __init__(self, title='', content=''):
		self['title'] = title
		self['keywords'] = []
		self['subsections'] = []
		self['figures'] = []
		self['tables'] = []
		self['content'] = content







