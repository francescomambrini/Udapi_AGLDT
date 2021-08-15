from udapi.core.files import Files
from lxml import etree
import logging


class AgldtFiles(Files):
    def __init__(self, files):
        super().__init__(filenames=files)

    def next_filehandle(self):
        """Go to the next file and retrun its filehandle or None (meaning no more files)."""
        filename = self.next_filename()
        if filename is None:
            fhandle = None
        else:
            logging.debug(f'Opening {filename}')
            x = etree.parse(filename)
            sents = x.xpath("//sentence")
            fhandle = (s for s in sents)
        self.filehandle = fhandle
        return fhandle
