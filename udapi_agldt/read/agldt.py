"""Reader for the AGLDT XML format
"""

from udapi.core.basereader import BaseReader
from udapi.core.root import Root
from udapi_agldt.util.agldtfiles import AgldtFiles
import logging


class Agldt(BaseReader):
    """A reader for plain-text sentences (one sentence per line) files."""

    def __init__(self, files='-', fix_cycles=False, **kwargs):
        super().__init__(files, **kwargs)
        self.files = AgldtFiles(files)
        self.fix_cycles = fix_cycles


    @staticmethod
    def is_multizone_reader():
        """Can this reader read bundles which contain more zones?.

        This implementation returns always False.
        """
        return False

    def read_tree(self, document=None):
        if self.filehandle is None:
            return None
        try:
            s = next(self.filehandle)
        except StopIteration:
            return None

        root = Root()
        nodes = [root]
        parents = [0]
        words = s.xpath("word")
        if len(words) == 0:
            return None
        root.sent_id = s.attrib.get("id")
        if s.xpath("word[@cite]"):
            has_cite = True
        else:
            has_cite = False

        for w in words:
            node = root.create_child()
            node.ord = int(w.attrib["id"])
            node.form = w.attrib["form"]
            node.feats = '_'
            h = int(w.attrib["head"]) if w.attrib.get("head") else 0 
            parents.append(h)
            node.deprel = w.attrib["relation"]
            postag = w.attrib.get("postag")
            lemma = w.attrib.get("lemma")
            if has_cite:
                c = w.attrib.get("cite")
                if c:
                    node.misc["Ref"] = c.split(":")[-1] if 'urn:' in c else c
            else:
                sub = s.attrib.get("subdoc")
                if sub:
                    node.misc["Ref"] = sub
            if w.attrib.get("insertion_id") or w.attrib.get("artificial"):
                node.misc["NodeType"] = 'Artificial'
                if postag:
                    node.upos = postag[0]
                    node.xpos = postag
                else:
                    node.upos = '_'
                    node.xpos = '_'
                node.lemma = lemma if lemma else '_'
            else:              
                try:
                    node.upos = postag[0]
                except (IndexError, TypeError) as e:
                    node.upos = 'x'
                    logging.warning(f"Node {node.address()} has no postag!")
                    
                node.xpos = postag
                node.lemma = lemma
            nodes.append(node)

        for i, n in enumerate(nodes[1:], 1):
            try:
                n.parent = nodes[parents[i]]
                
            except ValueError as e:
                if self.fix_cycles:
                    logging.warning(f"Ignoring a cycle for node {n.address()} (attaching to the root instead):\n")
                    n.parent = root
                else:
                    raise
            
        return root
