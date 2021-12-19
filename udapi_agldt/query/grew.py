"""
Invoke GREW-match to perform a query on a document. Although grew has a dedicated python library it is in fact easier
to invoke it as CLI service from within Python.
"""

from udapi.core.block import Block
import subprocess
import json


def run_grew(path_to_pattern, path_to_infile):
    try:
        j = subprocess.run(['grew', 'grep', '-pattern', path_to_pattern, '-i', path_to_infile],
                       capture_output=True, text=True)
    except FileNotFoundError:
        raise OSError('It seems that Grew is not properly installed on your system!')
    return j


class Grew(Block):

    def __init__(self, path_to_pattern_file, strict=True, mark=1, **kwargs):
        """
        Arguments
        ---------
        path_to_pattern_file : str
            path to file with the grew pattern to be matched
        strict: bool
            what to do with empty query (default: raise a custom NoResults exception)
        mark:
            matching nodes will be marked with `Mark=<mark>` in `node.misc`. Default=1.
        """
        super().__init__(**kwargs)
        self.pattern = path_to_pattern_file
        self._strict = strict
        self.matches = None

    def before_process_document(self, document):
        path_in = document.meta['loaded_from']
        res = run_grew(self.pattern, path_in)

        if res.returncode != 0:
            raise GrewError(res.stderr, message="Grew exited with a non-zero code")

        j = json.loads(res.stdout)

        if self._strict and not j:
            raise NoResults()

        mtchs = []
        for m in j:
            sid = m['sent_id']
            for v in m['matching']['nodes'].values():
                mtchs.append(f'{sid}#{v}')
        self.matches = mtchs

    def process_node(self, node):
        if node.address() in self.matches:
            node.misc['Mark'] = 1


class GrewError(Exception):
    """Exception raised when Grew exits with an error status.
        """

    def __init__(self, stderr, message="Grew error"):
        self.message = message + f'\nGrew error: {stderr}'
        super().__init__(self.message)


class NoResults(Exception):
    """Exception raised when Grew returns no results for a query.
    """

    def __init__(self, pattern_path, message="Your query returned no results!"):
        self.message = message
        super().__init__(self.message)
