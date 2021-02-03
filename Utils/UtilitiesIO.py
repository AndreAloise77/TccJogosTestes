import xml.etree.ElementTree as elementTree
import os

# Constants:
FILE_TYPE_XML = '.xml'


def get_single_file_in_dir(path: str):
    tree = ''
    for filename in os.listdir(path):
        if not filename.endswith(FILE_TYPE_XML):
            continue
        fullname = os.path.join(path, filename)
        tree = elementTree.parse(fullname)
    return tree


def get_all_files_in_dir_returns_list_element_tree(path: str):
    trees = []
    for filename in os.listdir(path):
        if not filename.endswith(FILE_TYPE_XML):
            continue
        fullname = os.path.join(path, filename)
        trees.append(elementTree.parse(fullname))
    return trees


def get_tree_root_returns_element(path: str):
    complete_tree = get_single_file_in_dir(path)
    root_tree = complete_tree.getroot()
    return root_tree
