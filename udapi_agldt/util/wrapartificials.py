"""
Simple scenario that wraps the node.form of an artificial within square brackets
if it isn't already wrapped
"""

from udapi.core.block import Block

class WrapArtificials(Block):

    def process_node(self, node):
        if node.misc['NodeType'] == 'Artificial':
            if not node.form.startswith('['):
                node.form = f'[{node.form}]'
