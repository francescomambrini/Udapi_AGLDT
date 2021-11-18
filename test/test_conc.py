from udapi_agldt.read.glaux import Glaux
from udapi.core.document import Document
from udapi.block.util.mark import Mark
from udapi_agldt.write.concordances import Concordances

doc = Document()
reader = Glaux(files='0059-017.xml')
reader.apply_on_document(doc)
marker = Mark(node='node.lemma == "δέω"', mark='conc')
marker.apply_on_document(doc)
nodes = doc.bundles[0].trees[0].descendants
print('done with the marking')

conc = Concordances(color='okblue', mark='conc')
conc.apply_on_document(doc)





