from lxml import etree


def writeObjs2xml(xml_file, objs, obj_name):
    """
    Write a list of objects (e.g., Question post or Comment) to an XML file.
    """
    root = etree.Element(obj_name, attrib={'count': str(len(objs))})

    for obj in objs:
        try:
            etree.SubElement(root, 'row', attrib=obj.to_dict_s())
        except Exception as e:
            print ('***** Error in writeObjs2xml() *****', e, ':', obj.to_dict_s())

    tree = etree.ElementTree(root)
    tree.write(xml_file, pretty_print=True, xml_declaration=True, encoding='utf-8')


def writeDictList2xml(xml_file, dict_list, item_name):
    """
    Write a list of dicts (each dict is an info unit) to an XML file.
    """
    root = etree.Element(item_name, attrib={'count': str(len(dict_list))})

    for _dict in dict_list:
        try:
            etree.SubElement(root, 'row', attrib=_dict)
        except Exception as e:
            print ('***** Error in writeDictList2xml() *****', e, ':', _dict)

    tree = etree.ElementTree(root)
    tree.write(xml_file, pretty_print=True, xml_declaration=True, encoding='utf-8')
