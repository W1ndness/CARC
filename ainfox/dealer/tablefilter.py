from ainfox.dealer import tagfilter
from ainfox.webpage import webpage


class TableFilter(tagfilter.TagFilter):
    def __init__(self, page: webpage.WebPage):
        super().__init__(page)
        self.__tag = "table"

    def filtration(self):
        tables = self.page.soup.find_all('table')
        return tables