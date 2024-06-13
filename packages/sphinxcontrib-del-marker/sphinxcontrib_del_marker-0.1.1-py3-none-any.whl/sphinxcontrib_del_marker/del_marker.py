"""
# @Project sphinxcontrib-del-marker
# @File    del_marker.py
# @Author  MT308
# @Date    2024/6/9 18:49
"""

from docutils import nodes
from docutils.parsers.rst import Directive


class DelMarkerDirective(Directive):
    # this enables content in the directive
    has_content = True

    def run(self):
        node = nodes.raw('', f'<del>{self.content[0]}</del>', format='html')
        return [node]
