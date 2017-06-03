import sys
from parser import Parser

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print("Usage: python3 parser.py <path-to-latex-file>")
	else:
		parser = Parser(sys.argv[1])
		thesis = parser.parse_thesis()

		print(thesis)
