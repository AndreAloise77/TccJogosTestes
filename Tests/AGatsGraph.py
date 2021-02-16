from typing import List

from graphviz import Digraph
from graphviz import Source

from Tests.GatsGraph import GatsGraph
from Utils.UtilitiesTestFilePathConstants import UtilitiesTestFilePathConstants


class AGats:
    def __init__(self):
        self.AGats: Digraph = Digraph()
        self.FileName: str = ''

    def create_agats(self, gats_list: List[GatsGraph], file_name: str):
        for gats in gats_list:
            self.AGats = gats
        self.FileName = file_name

    def export_agats(self):
        self.AGats.render(UtilitiesTestFilePathConstants.AGATS_FORMAT_FILE_STRUCTURE
                          .format(UtilitiesTestFilePathConstants.TEST_OUTPUT_PATH,
                                  UtilitiesTestFilePathConstants.TEST_OUTPUT_AGATS_PATH,
                                  self.FileName,
                                  UtilitiesTestFilePathConstants.GRAPHVIZ_EXTENSION_FILE),
                          view=True)

    def read_agats_from_file(self, file_name: str):
        self.AGats = Source.from_file(UtilitiesTestFilePathConstants.AGATS_FORMAT_FILE_STRUCTURE
                                      .format(UtilitiesTestFilePathConstants.TEST_OUTPUT_PATH,
                                              UtilitiesTestFilePathConstants.TEST_OUTPUT_AGATS_PATH,
                                              file_name,
                                              UtilitiesTestFilePathConstants.GRAPHVIZ_EXTENSION_FILE))
        self.AGats.render(view=True)
