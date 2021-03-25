import os
import xml.etree.ElementTree as elementTree
from typing import List
from xml.etree.ElementTree import ElementTree

import Utils.UtilitiesAGatsFileConstants
import Utils.UtilitiesFilePathConstants

# Constants:
UTILITIES_CONSTANTS = Utils.UtilitiesFilePathConstants.UtilitiesFilePathConstants
UTILITIES_AGATS_CONSTANTS = Utils.UtilitiesAGatsFileConstants.UtilitiesAGatsFileConstants
OPEN_FILE_TO_OVERRIDE: str = 'w'


def get_single_file_in_dir(path: str):
    tree = ''
    for filename in os.listdir(path):
        if not filename.endswith(UTILITIES_CONSTANTS.XML_EXTENSION_FILE):
            continue
        fullname = os.path.join(path, filename)
        tree = elementTree.parse(fullname)
    return tree


def build_tree_by_filename(path: str) -> ElementTree:
    tree: ElementTree = elementTree.parse(path)
    return tree


def get_fullname_from_all_files_in_dir(path: str) -> List[str]:
    absolute_path: str = os.path.abspath(path)
    filename_list: List[str] = []
    for filename in os.listdir(absolute_path):
        if not filename.endswith(UTILITIES_CONSTANTS.XML_EXTENSION_FILE):
            continue
        fullname = os.path.join(absolute_path, filename)
        filename_list.append(fullname)
    return filename_list


def get_filename_in_dir(directory: str, fullname: str) -> str:
    absolute_path: str = os.path.abspath(directory)
    tuple_path: List[str] = fullname.split(absolute_path)
    file_name: str = tuple_path[1]
    return file_name


def get_all_files_in_dir_returns_list_element_tree(path: str) -> List[ElementTree]:
    trees: List[ElementTree] = []
    for filename in os.listdir(path):
        if not filename.endswith(UTILITIES_CONSTANTS.XML_EXTENSION_FILE):
            continue
        fullname = os.path.join(path, filename)
        trees.append(elementTree.parse(fullname))
    return trees


def get_tree_root_returns_element(path: str):
    complete_tree = get_single_file_in_dir(path)
    root_tree = complete_tree.getroot()
    return root_tree


def read_invalid_edges_file(invalid_file_name: str) -> List[str]:
    file = open(UTILITIES_CONSTANTS.INVALID_EDGES_FILES_STRUCTURE
                .format(UTILITIES_CONSTANTS.READ_INVALID_EDGES_FILES_DIRECTORY,
                        invalid_file_name,
                        UTILITIES_CONSTANTS.TEXT_EXTENSION_FILE))

    file_lines_list: List[str] = file.readlines()
    file_lines_list = __clean_list(file_lines_list)
    return file_lines_list


def __clean_list(file_list: List[str]):
    returned_list: List[str] = []
    for line in file_list:
        value: str = line.replace(UTILITIES_AGATS_CONSTANTS.OPEN_BRACKETS, '')
        value = value.replace(UTILITIES_AGATS_CONSTANTS.QUOTATION_MARK, '')
        value = value.replace(UTILITIES_AGATS_CONSTANTS.JUMP_LINE, '')
        value = value.replace(UTILITIES_AGATS_CONSTANTS.CLOSE_BRACKETS, '')
        returned_list.append(value)

    return returned_list


def import_agats_file_to_list(path: str, folder_name: str, file_name: str) -> List[str]:
    file = open(path.format(UTILITIES_CONSTANTS.OUTPUT_PATH,
                            UTILITIES_CONSTANTS.OUTPUT_AGATS_PATH,
                            folder_name, file_name,
                            UTILITIES_CONSTANTS.GRAPHVIZ_EXTENSION_FILE))

    file_lines_list: List[str] = file.readlines()
    return file_lines_list


def write_on_invalid_file(invalid_edge_ids: str):
    filename = UTILITIES_CONSTANTS.INVALID_EDGE_FILENAME
    invalid_list: List[str] = read_invalid_edges_file(filename)
    is_unique: bool = invalid_edge_ids not in invalid_list
    if is_unique:
        file_name = '{}{}'.format(filename, UTILITIES_CONSTANTS.TEXT_EXTENSION_FILE)
        file_path_and_name = os.path.join(UTILITIES_CONSTANTS.READ_INVALID_EDGES_FILES_DIRECTORY, file_name)
        with open(file_path_and_name, 'a') as file:
            file.write(invalid_edge_ids)
            file.write('\n')


def write_on_temp_file(had_read_edge_file: bool, directory: str, file_name: str):
    data: str = str(had_read_edge_file)
    file_path_and_name = os.path.join(directory, file_name)
    with open(file_path_and_name, OPEN_FILE_TO_OVERRIDE) as file:
        file.write(data)


def get_dir_base_name(path):
    folder_name = __get_sub_dir(path)
    base_name = os.path.basename(folder_name)
    return base_name


def __get_sub_dir(directory):
    folders: List[str] = []
    for x in os.walk(directory):
        folders.append(x[0])

    if len(folders) > 0:
        return folders[-1]
    else:
        raise Exception("There are no folders on Directory: '{}'".format(directory))
