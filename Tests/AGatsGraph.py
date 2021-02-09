from typing import List

from graphviz import Digraph

from Tests.GatsGraph import GatsGraph


class AGats:
    def __init__(self):
        self.AGats: Digraph = Digraph()
        self.FileName: str = ''

    def create_agats(self, gats_list: List[GatsGraph], file_name: str):
        for gats in gats_list:
            self.AGats = gats
        self.FileName = file_name

    def print_agats(self):
        self.AGats.render('test-output/{}.gv'.format(self.FileName), view=True)
