#!/usr/bin/env python

import sys
import os

sys.path.insert(0,os.path.expanduser('~/Documents/sync/progetti/Udapi_AGLDT/'))

from udapi_agldt.read.agldt import Agldt
from udapi.core.document import Document

from glob import glob
from tqdm import tqdm
import logging

logging.disable(logging.WARNING)

glaux_dir = os.path.expanduser('/home/francesco/Documents/sync/data/corpora/gorman-trees-1.0.1/')
assert os.path.isdir(glaux_dir), "Somethin is wrong with Glaux path"
fs = glob(f'{glaux_dir}/public/xml/*.xml')


for f in tqdm(fs):
    doc = Document()
    reader = Agldt(f, fix_cycles=True)
    reader.apply_on_document(doc)
