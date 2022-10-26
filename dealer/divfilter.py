import re

from tagfilter import TagFilter
import webpage


class DivFilter(TagFilter):
    def __init__(self, page: webpage.WebPage):
        super().__init__(page)
        self.__tag = "div"

    def filtration(self):
        pattern = r'[\S]*?(content|main)[\S]*?'
        divs = self.page.soup.find_all('div', id=re.compile(pattern))
        return divs
