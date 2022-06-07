# udapy -s read.Conllu files='!*.conllu' \
#   util.Filter mark=pron keep_tree_if_node="node.upos == 'p' and node.deprel=='SBJ' and node.parent.upos=='v'" \
#   > ~/Desktop/res.conllu

import os
from udapi.block.read.conllu import Conllu
from udapi.block.util.filter import Filter
from udapi.core.document import Document


class Query(Filter):
    """c
    Simple subclass of util.filter.Filter that only executes keep_tree_if_node, but accepts python functions as
    its argument
    """
    def __init__(self, func, mark=None):
        """
        :param func: a Python function that accets one argument of the type core.Node
        :param mark: string to be added to the misc column (Mark=:str)
        """
        super().__init__(mark=mark)
        self.function = func

    def process_tree(self, tree):
        root = tree

        found = False
        for node in tree.descendants:
            if self.function(node):
                found = True
                if self.mark:
                    node.misc['Mark'] = self.mark
                else:
                    return
        if not found:
            tree.remove()
        return


class CorpusQuery():
    def __init__(self, root, pattern="*.conllu", mark=None):
        self._filepath = "!" + os.path.join(root, pattern)
        self.mark = mark
        self.document = Document()
        # self.document.load_conllu(filename=self._filepath)
        self._reader = Conllu(files=self._filepath)
        self._reader.apply_on_document(self.document)

    def run_query(self, function):
        q = Query(function, self.mark)
        q.apply_on_document(self.document)

    def write_results(self, writer_class, outfile, **kwargs):
        from importlib import import_module
        writer = getattr(import_module(f"udapi.block.write.{writer_class.lower()}"), writer_class)
        with open(outfile, 'w') as out:
            wrt = writer(filehandle=out, **kwargs)
            wrt.apply_on_document(self.document)
