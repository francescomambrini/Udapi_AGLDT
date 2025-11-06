#!/usr/bin/env python

"""Convert a file from Gorman/AGDT/Pedalion XML to CoNLL-U

Usage:
    python convert_file.py <file(s)>

Keyword arguments:
file(s) -- path to XML file to convert (or glob pattern with XML files) 
Return: writes conllu files with the same base name as the input file(s) + '.conllu', in the current working dir
"""

from glob import glob
import sys
import os
import logging

# For Gorman/AGDT:
from udapi_agldt.read.agldt import Agldt

# For Pedalion:
from udapi_agldt.read.glaux import Glaux

from udapi.core.document import Document

input_pat = sys.argv[1]

fs = glob(input_pat)
print(len(fs))

if not fs:
    logging.error("No file found at the specified path")
    sys.exit()

for f in fs:
    print(f'working with {f}')
    doc = Document()

    # substitute Glaux to Agldt for the Glaux reader; but keep `fix_cycle=True`!
    reader = Agldt(f, fix_cycles=True)
    reader.apply_on_document(doc)

    base_name = os.path.basename(f)
    out_name = os.path.splitext(base_name)[0] + '.conllu'

    doc.store_conllu(out_name)
