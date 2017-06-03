import sys
import json
from thesis_parsing import Splitter, Extracter, Thesis, Chapter, Section

class Parser(object):
	def __init__(self, filename):
		self.filename = filename

	def parse(self):
		thesis = Thesis()

		with open(self.filename, 'r') as f:
			thesis_raw = f.read()

		# chapter
		chapters = Splitter.split_chapters(thesis_raw)
		for chapter in chapters:
			chapter_title = Extracter.extract_title(chapter)
			chapter_data = Chapter(title=chapter_title)

			# section
			sections = Splitter.split_sections(chapter)
			for section in sections:
				section_title = Extracter.extract_title(section)
				section_data = Section(title=section_title)

				# subsection
				subsections = Splitter.split_subsections(section)
				for subsection in subsections:
					subsection_title = Extracter.extract_title(subsection)
					subsection_data = Section(title=subsection_title)

					# subsubsection
					subsubsections = Splitter.split_subsubsections(subsection)
					for subsubsection in subsubsections:
						subsubsection_title = Extracter.extract_title(subsubsection)
						subsubsection_data = Section(title=subsubsection_title)
						#print('\t\t{}'.format(subsubsection_title))
						subsection_data['subsections'].append(subsubsection_data)

					section_data['subsections'].append(subsection_data)

				chapter_data['sections'].append(section_data)

			thesis['chapters'].append(chapter_data)

		print(json.dumps(thesis))
		#print(jsonpickle.encode(thesis))


if __name__ == '__main__':
	if len(sys.argv) != 2:
		print("Usage: python3 parser.py <latex-file>")
	else:
		parser = Parser(sys.argv[1])
		parser.parse()





