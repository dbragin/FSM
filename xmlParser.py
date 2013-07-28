from xml.etree.ElementTree import XML, fromstring, tostring
import diagramm
from xml.etree import ElementTree 

class XmlUtil:
    @staticmethod
    def readXml(xmlSource,typematrix=None):
        d = diagramm.Diagramm()
        xml = fromstring(xmlSource)

        if(typematrix != None): 
          gettype = lambda x:typematrix[x]()
        else:
          gettype = lambda x:x

        elements = xml.findall(".//Element")
	for e in elements:
            uid = e.find('.//Id').text.strip()
            elType = gettype(e.get("type"))
            d.addElement(elType, uid)
        
	links = xml.findall(".//*Link")
        for l in links:
            uid = l.find('./Id').text.strip()
            sourceUid =  l.find('.//Source/Id').text.strip()
            targetUid =  l.find('.//Sink/Id').text.strip()
            d.addLink(uid, sourceUid, targetUid)
        
        return d

    @staticmethod
    def dictToXml(dict):
        root = ElementTree.Element("errors")
        ElementTree.SubElement(root,"count").text = len(dict).__str__()
        list = ElementTree.SubElement(root,"list")
        for entity in dict:
                er = ElementTree.SubElement(list,"error")
                ElementTree.SubElement(er, "description").text = entity['text']
                ElementTree.SubElement(er, "Element").text = entity['id']
        return ElementTree.tostring(root,encoding='utf-8')
