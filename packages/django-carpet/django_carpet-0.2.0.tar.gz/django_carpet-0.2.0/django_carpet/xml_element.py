from xml.etree import cElementTree
from xml.etree.ElementTree import ParseError

from typing import List, Union


class XMLParseError(ParseError):
    pass


class XMLElement:

    @staticmethod
    def parse_string(raw: str):
        """
        Parses a string a return an instance of XMLElement
        :param raw: The XML data in the string format
        :return: an Instance of XMLElement
        """
        try:
            return XMLElement(cElementTree.fromstring(raw))
        except ParseError:
            raise XMLParseError()  # noqa: B904
        except TypeError:
            raise XMLParseError()  # noqa: B904
        
    @staticmethod
    def try_parse_string(raw: str) -> Union['XMLElement', None]:
        """
        Parses a string a return an instance of XMLElement
        If the raw cannot be parsed, None is returned
        :param raw: The XML data in the string format
        :return: an Instance of XMLElement
        """
        try:
            return XMLElement.parse_string(raw)
        except XMLParseError:
            return None

    def __init__(self, element):
        self.element = element

    def __str__(self):
        return "<{t} attrib={a} childrenCount={c} />".format(t=self.tag, c=self.children_count, a=self.attrib)

    @property
    def text(self) -> str:
        """The text property of the native xml element"""
        return self.element.text

    @property
    def attrib(self) -> dict:
        """The attribute element of the native xml element"""
        return self.element.attrib

    @property
    def tag(self) -> str:
        """The name of the tag of the native xml element. Namespaces will be removed, if any."""
        splitted = self.element.tag.split("}")
        return splitted[len(splitted) - 1]

    @property
    def full_tag(self) -> str:
        """The the tag of the native xml element, including the namespaces, if any"""
        return self.element.tag

    @property
    def children(self):
        """A list containing the children of the element"""
        children: List[XMLElement] = []
        for child in list(self.element):
            children.append(XMLElement(child))
        return children

    @property
    def children_count(self) -> int:
        """The number of children"""
        return len(self.element)

    @property
    def has_child(self) -> bool:
        """Whether the element has any children"""
        return len(self.element) > 0

    @property
    def has_attrib(self) -> bool:
        """Checks if the element has any attributes"""
        return len(self.attrib) > 0

    def iter(self, target_tag: str):
        """Similar to the children property"""
        iterations = self.element.iter(target_tag)
        children: List[XMLElement] = []
        for i in iterations:
            children.append(XMLElement(i))
        return children

    def find_all(self, target_tag: str):
        """Finds all child elements whose tag name matches that of the target tag"""
        iterations = self.element.findall(target_tag)
        children: List[XMLElement] = []
        for i in iterations:
            children.append(XMLElement(i))
        return children

    def find(self, target_tag: str):
        """Finds the first child whose tag name matches that of the target tag"""
        found: XMLElement = XMLElement(self.element.find(target_tag))
        return found

    def to_dict(self) -> dict:
        """Converts the XML element and its children to a dict"""        

        x: dict = {
            "tag": self.full_tag            
        }

        if self.has_attrib:
            x["attributes"] = self.attrib

        if self.has_child:
            children = self.children
            x["children"] = []

            for c in children:
                x["children"].append(c.to_dict())        
        elif self.text is not None:
            parsed = XMLElement.try_parse_string(self.text)
            if parsed is not None:
                x['children'] = [parsed.to_dict()]
            else:
                x["text"] = self.text

        return x