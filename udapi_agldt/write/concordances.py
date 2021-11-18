from udapi.core.basewriter import BaseWriter
from udapi_agldt.util.udapi_concindex import UdapiConcordanceIndex


class Concordances(BaseWriter):
    def __init__(self, files='-', color=None, mark='1', width=80, lines=25, **kwargs):
        self._color = color
        self._mark = mark
        self._width = width
        self._lines = lines

        super().__init__(files, **kwargs)

    def process_document(self, document):
        nodes = [n for n in document.nodes]
        concindex = UdapiConcordanceIndex(nodes, self._mark, self._color, self._width)
        concindex.print_concordance('yes', width=self._width, lines=self._lines)
