from tests.ditest import DependencyInjectionTestBase
from mock import Mock
import datetime


class XmlFormatTests(DependencyInjectionTestBase):

    def setUp(self):
        super(XmlFormatTests, self).setUp()

    def test_serialize_item_returns_string_with_xml_header(self):
        prolog = '<?xml version="1.0" encoding="UTF-8"?>'
        doc = '<prov:document'
        from niprov.formatxml import XmlFormat
        form = XmlFormat(self.dependencies)
        out = form.serializeSingle(self.aFile())
        self.assertIn(prolog, out)
        self.assertIn(doc, out)

    def test_serialize_list_creates_entity_for_each_file(self):
        from niprov.formatxml import XmlFormat
        form = XmlFormat(self.dependencies)
        out = form.serializeList([self.aFile(), self.aFile(), self.aFile()])
        self.assertEqual(3, out.count('<prov:entity'))

    def test_has_PROV_namespace(self):
        from niprov.formatxml import XmlFormat
        form = XmlFormat(self.dependencies)
        out = form.serializeSingle(self.aFile())
        docline = [l for l in out.split('\n') if 'prov:doc' in l][0]
        prov = 'http://www.w3.org/ns/prov#'
        nsattr = 'xmlns:prov="{0}"'.format(prov)
        self.assertIn(nsattr, docline)

    def test_has_NFO_namespace(self):
        from niprov.formatxml import XmlFormat
        form = XmlFormat(self.dependencies)
        out = form.serializeSingle(self.aFile())
        docline = [l for l in out.split('\n') if 'prov:doc' in l][0]
        nfo = 'http://www.semanticdesktop.org/ontologies/2007/03/22/nfo#'
        nsattr = 'xmlns:nfo="{0}"'.format(nfo)
        self.assertIn(nsattr, docline)

    def test_Entity_has_id(self):
        from niprov.formatxml import XmlFormat
        form = XmlFormat(self.dependencies)
        aFile = self.aFile()
        out = form.serializeSingle(aFile)
        from xml.dom.minidom import parseString
        dom = parseString(out)
        entity = dom.getElementsByTagName("prov:entity")[0]
        self.assertEqual(entity.attributes['id'].value, 'niprov:file0')

    def test_serialize_file_entity_has_fileUrl_prop(self):
        from niprov.formatxml import XmlFormat
        form = XmlFormat(self.dependencies)
        aFile = self.aFile()
        out = form.serializeSingle(aFile)
        from xml.dom.minidom import parseString
        dom = parseString(out)
        entity = dom.getElementsByTagName("prov:entity")[0]
        targetPropElements = entity.getElementsByTagName("nfo:fileUrl")
        self.assertEqual(1, len(targetPropElements))
        self.assertEqual(str(aFile.location.toUrl()), 
            self.getElementContent(targetPropElements[0]))

    def test_serialize_file_entity_has_fileUrl_prop(self):
        from niprov.formatxml import XmlFormat
        form = XmlFormat(self.dependencies)
        aFile = self.aFile()
        out = form.serializeSingle(aFile)
        from xml.dom.minidom import parseString
        dom = parseString(out)
        entity = dom.getElementsByTagName("prov:entity")[0]
        targetPropElements = entity.getElementsByTagName("nfo:fileUrl")
        self.assertEqual(1, len(targetPropElements))
        self.assertEqual(str(aFile.location.toUrl()), 
            self.getElementContent(targetPropElements[0]))

    def test_serialize_file_entity_has_fileSize_prop(self):
        from niprov.formatxml import XmlFormat
        form = XmlFormat(self.dependencies)
        aFile = self.aFile()
        out = form.serializeSingle(aFile)
        from xml.dom.minidom import parseString
        dom = parseString(out)
        entity = dom.getElementsByTagName("prov:entity")[0]
        targetPropElements = entity.getElementsByTagName("nfo:fileSize")
        self.assertEqual(1, len(targetPropElements))
        self.assertEqual(str(56789), 
            self.getElementContent(targetPropElements[0]))

    def test_serialize_file_entity_has_fileLastModified_prop(self):
        from niprov.formatxml import XmlFormat
        form = XmlFormat(self.dependencies)
        aFile = self.aFile()
        out = form.serializeSingle(aFile)
        from xml.dom.minidom import parseString
        dom = parseString(out)
        entity = dom.getElementsByTagName("prov:entity")[0]
        targetPropElements = entity.getElementsByTagName("nfo:fileLastModified")
        self.assertEqual(1, len(targetPropElements), 'Should have exactly one match')
        self.assertEqual(aFile.provenance['created'].isoformat(), 
            self.getElementContent(targetPropElements[0]))

    def test_serialize_file_entity_has_hash(self):
        from niprov.formatxml import XmlFormat
        form = XmlFormat(self.dependencies)
        aFile = self.aFile()
        out = form.serializeSingle(aFile)
        from xml.dom.minidom import parseString
        dom = parseString(out)
        entity = dom.getElementsByTagName("prov:entity")[0]
        #hasHash + FileHash with matching id
        targetPropElements = entity.getElementsByTagName("nfo:hasHash")
        self.assertEqual(1, len(targetPropElements))
        hashref = self.getElementContent(targetPropElements[0])
        allHashes = dom.getElementsByTagName("nfo:FileHash")
        hashesWithId = [e for e in allHashes if e.attributes['id'].value==hashref]
        self.assertEqual(1, len(hashesWithId))
        hashElement = hashesWithId[0]
        #algorithm
        targetPropElements = hashElement.getElementsByTagName("nfo:hashAlgorithm")
        self.assertEqual(1, len(targetPropElements), 'Should have exactly one match')
        self.assertEqual('MD5', 
            self.getElementContent(targetPropElements[0]))
        #value
        targetPropElements = hashElement.getElementsByTagName("nfo:hashValue")
        self.assertEqual(1, len(targetPropElements), 'Should have exactly one match')
        self.assertEqual(aFile.provenance['hash'], 
            self.getElementContent(targetPropElements[0]))

    def test_FileHash_id_follows_sensible_format(self):
        from niprov.formatxml import XmlFormat
        form = XmlFormat(self.dependencies)
        aFile = self.aFile()
        out = form.serializeSingle(aFile)
        from xml.dom.minidom import parseString
        dom = parseString(out)
        entity = dom.getElementsByTagName("prov:entity")[0]
        targetPropElements = entity.getElementsByTagName("nfo:hasHash")
        self.assertEqual(1, len(targetPropElements))
        hashref = self.getElementContent(targetPropElements[0])
        self.assertEqual(entity.attributes['id'].value+'.hash', hashref)




    def getElementContent(self, element):
        rc = []
        for node in element.childNodes:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        return ''.join(rc)

    def aFile(self):
        somefile = Mock()
        somefile.provenance = {}
        somefile.provenance['size'] = 56789
        somefile.provenance['created'] = datetime.datetime.now()
        somefile.provenance['hash'] = 'abraca777'
        somefile.location.toUrl.return_value = 'xkcd://HAL/location.loc'
        return somefile