#!/usr/bin/env python

import sys
import os

sys.path.insert(0,os.path.expanduser('~/Documents/sync/progetti/Udapi_AGLDT/'))

from udapi_agldt.read.glaux import Glaux
from udapi.core.document import Document

from glob import glob
from tqdm import tqdm
import logging

logging.disable(logging.WARNING)

glaux_dir = os.path.expanduser('~/Documents/sync/data/corpora/glaux')
assert os.path.isdir(glaux_dir), "Somethin is wrong with Glaux path"
fs = glob(f'{glaux_dir}/xml/*.xml')


for f in tqdm(fs):
    fname = f.split('/')[-1][:-4]
    doc = Document()
    reader = Glaux(f, fix_cycles=True)
    reader.apply_on_document(doc)
