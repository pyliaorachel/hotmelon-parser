import sys
import json
from thesis_parsing import Splitter, Extracter, Thesis, Chapter, Section

class Parser(object):
	def __init__(self, filename):
		self.filename = filename

	def parse_sections(self, raw_text, level=0, max_level=2):
		if level > max_level:
			return

		section_list = []

		sections = Splitter.split_sections(raw_text, level=level)
		for section in sections:
			section_title = Extracter.extract_title(section)
			section_data = Section(title=section_title)
			if level + 1 <= max_level:
				section_data['subsections'] = self.parse_sections(section, level=level+1, max_level=max_level)

			section_list.append(section_data)

		return section_list

	def parse_chapters(self, raw_text):
		chapter_list = []

		chapters = Splitter.split_chapters(raw_text)
		for chapter in chapters:
			chapter_title = Extracter.extract_title(chapter)
			chapter_data = Chapter(title=chapter_title)
			chapter_data['sections'] = self.parse_sections(chapter)

			chapter_list.append(chapter_data)

		return chapter_list

	def parse_thesis(self):
		with open(self.filename, 'r') as f:
			thesis_raw = f.read()

		thesis_title = Extracter.extract_thesis_title(thesis_raw)
		thesis = Thesis(title=thesis_title)
		
		thesis['chapters'] = self.parse_chapters(thesis_raw)
		thesis['authors'] = Extracter.extract_authors(thesis_raw)

		print(json.dumps(thesis))

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print("Usage: python3 parser.py <latex-file>")
	else:
		parser = Parser(sys.argv[1])
		parser.parse_thesis()





