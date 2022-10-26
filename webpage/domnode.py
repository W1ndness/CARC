import re
from typing import List

import bs4


class Node:
    def __init__(self, node):
        if not issubclass(type(node), bs4.element.PageElement):
            raise TypeError

        self.node = node
        self.nodeType = type(node)
        self.nodeName = node.name
        if isinstance(node, bs4.element.Tag):
            self.nodeContent = node.contents[0]
        else:
            self.nodeContent = node.string

        self.children = None
        self.parents = None

        self.getChildren()
        self.getParents()

        self.__pattern = re.compile(r'<()>()<()>')

    def __str__(self) -> str:
        return self.nodeContent

    def getChildren(self) -> List[bs4.element.PageElement]:
        ret = list(self.node.children)
        return ret if ret else None

    def getParents(self) -> List[bs4.element.PageElement]:
        ret = list(self.node.parents)
        return ret if ret else None
