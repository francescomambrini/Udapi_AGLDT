#!/usr/bin/env python

from udapi_agldt.read.agldt import Agldt
from udapi.core.root import Root
import logging


class Papygreek(Agldt):

    def __init__(self, files='-', use_version='reg', **kwargs):
        self._version = use_version
        if self._version and self._version not in ['orig', 'reg']:
            raise ValueError(f'`use_version` must be either `orig` (original) or `reg` (regularized)')
        super().__init__(files, **kwargs)

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
            node.form = w.attrib[f"form_{self._version}"]
            node.feats = '_'
            h = int(w.attrib[f"head_{self._version}"]) if w.attrib.get(f"head_{self._version}") else 0
            parents.append(h)
            node.deprel = w.attrib[f"relation_{self._version}"] if w.attrib.get(f"head_{self._version}") else 'NA'
            postag = w.attrib.get(f"postag_{self._version}")
            if postag:
                postag = postag.ljust(9, '-')
            else:
                postag = 'x' + 8 * '-'

            lemma = w.attrib.get(f"lemma_{self._version}")
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
                    node.xpos = 'x' + 8 * '-'
                node.lemma = lemma if lemma else '_'
            else:
                try:
                    node.upos = postag[0]
                except (IndexError, TypeError) as e:
                    node.upos = 'x'
                    node.xpos = 'x' + 8 * '-'
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

            except IndexError:
                logging.error(f'Head value for {n.address()} not in sentence\'s range ({h})')
                n.parent = root

        return root
