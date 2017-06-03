import sys
from plasTeX.TeX import TeX
from plasTeX.Renderers.XHTML import Renderer

Renderer().render(TeX(file=sys.argv[1]).parse())