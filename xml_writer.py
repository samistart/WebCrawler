import lxml.etree as etree
import xml.sax.saxutils as saxutils
import config


class XmlWriter:

    def __init__(self, project_name):
        self.root = etree.Element(project_name)

    def write(self, path_str):
        path_list = path_str.split("/")
        self.add_to_elm(path_list, self.root)
        self.write_to_file()

    @staticmethod
    def get_child_or_create(parent, child_name):
        for ele in parent.getiterator():
            if ele.tag == child_name:
                return ele
        return etree.SubElement(parent, child_name)

    @staticmethod
    def sanitise_tag(tag):
        tag = tag.replace('@', '')
        tag = tag.replace(',', '')
        tag = tag.replace(';', '')
        tag = tag.replace('=', '')
        if tag[0].isdigit():
            tag = 'n' + tag
        return tag

    @staticmethod
    def add_to_elm(path_list, elm):
        tag = ''
        while tag == '' and len(path_list) != 0:
            tag = path_list[0]
            path_list = path_list[1:]
        if tag == '':
            return
        xml_safe_tag = XmlWriter.sanitise_tag(tag)
        try:
            child = XmlWriter.get_child_or_create(elm, xml_safe_tag)
            XmlWriter.add_to_elm(path_list, child)
        except:
            print("Cannot add tag to tree: " + xml_safe_tag)

    def write_to_file(self):
        tree = etree.ElementTree(self.root)
        tree.write(self.root.tag + ".xml", pretty_print=True)

