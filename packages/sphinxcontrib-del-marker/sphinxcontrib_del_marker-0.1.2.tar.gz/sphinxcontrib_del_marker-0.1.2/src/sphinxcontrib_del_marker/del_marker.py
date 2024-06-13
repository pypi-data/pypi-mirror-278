"""
# @Project sphinxcontrib-del-marker
# @File    del_marker.py
# @Author  MT308
# @Date    2024/6/9 18:49
"""

from docutils import nodes
from docutils.parsers.rst import Directive


class DelNode(nodes.General, nodes.Element):
    pass


def visit_del_node(self, node):
    self.body.append(self.starttag(node, 'del'))


def depart_del_node(self, node):
    self.body.append('</del>')


class DelMarkerDirective(Directive):
    # this enables content in the directive
    has_content = True

    def run(self):
        paragraph_node = nodes.paragraph()

        self.state.nested_parse(self.content, self.content_offset, paragraph_node)
        del_node_instance = DelNode()
        del_node_instance += paragraph_node.children
        return [del_node_instance]
