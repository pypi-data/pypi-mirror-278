from __future__ import annotations;

from lxml import etree;
import xml.etree.ElementTree as ET;

from AlmaxUtils import Generic as AUG;
from AlmaxClasses.Result import Result;

class XmlObj:
    '''Classe da utilizzare per estendere una classe che rappresenti un xml con le sue proprietà'''
    def __init__(self):
        pass;

    def GetAttributesForXml(self) -> list:
        attributesValues = [];
        for attr in dir(self):
            if not callable(getattr(self, attr)) and not attr.startswith("_"):
                attributesValues.append(XmlTagAttribute(attr, getattr(self, attr)));
        return attributesValues;
 
    def ConvertToXml(self, parent: ET.Element) -> ET.Element:
        tag = XmlTag(self.__class__.__name__.lower(), self.GetAttributesForXml());
        return tag.ConvertToXmlElement(parent);

class XmlTag:
    '''Classe che facilita la creazione di un elemento tag, da usare in casi un po' più defficili da gestire rispetto a XmlObj'''
    def __init__(self, tagName: str, tagAttributes: list):
        self.__TagName = tagName;
        if AUG.AllElementsHaveSameClass(tagAttributes, XmlTagAttribute):
            self.__TagAttributes = tagAttributes;
        else:
            raise ValueError("All elements in tagAttributes must be instances of XmlTagAttribute");

    @staticmethod
    def FromTouplesList(tagName: str, tagAttributes: list) -> XmlTag:
        allAttr = [];
        for attrName,attrValue in tagAttributes:
            allAttr.append(XmlTagAttribute(attrName, attrValue));
        return XmlTag(tagName, allAttr);

    def ConvertToXmlElement(self, parent: ET.Element) -> ET.Element:
        attribElements = {};
        childs = [];
        for attribute in self.__TagAttributes:
            if isinstance(attribute.Value, list):
                childs.append(attribute.Value);
            else:
                attribElements[attribute.Name] = str(attribute.Value);
        elemForParent = ET.SubElement(parent, self.__TagName, attrib=attribElements);

        for child in childs:
            for elem in child:
                elem.ConvertToXml(elemForParent);

        return elemForParent;

class XmlTagAttribute:
    def __init__(self, attributeName: str, attributeValue: str):
        self.__AttributeName = attributeName;
        self.__AttributeValue = attributeValue;

    @property
    def Name(self) -> str:
        return str(self.__AttributeName);

    @property
    def Value(self):
        return self.__AttributeValue;

def XML_ValidateXSD(xml_path: str, xsd_path: str) -> Result:
    with open(xsd_path, 'r') as schema_file:
        schema = etree.XMLSchema(etree.parse(schema_file));
    with open(xml_path, 'r') as xml_file:
        doc = etree.parse(xml_file);
    try:
        schema.assertValid(doc);
        return Result(True, "XML document is valid");
    except etree.DocumentInvalid as e:
        return Result(False, f"XML document is invalid: {e}");