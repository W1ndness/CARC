import re

from ainfox.webpage import webpage
from ainfox.dealer import tagfilter

class DivFilter(tagfilter.TagFilter):
    def __init__(self, page: webpage.WebPage):
        super().__init__(page)
        self.__tag = "div"

    def filtration(self):
        pattern = r'[\S]*?(content|main)[\S]*?'
        divs = self.page.soup.find_all('div', id=re.compile(pattern))
        return divs
