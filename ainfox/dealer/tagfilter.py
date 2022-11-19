from ainfox.webpage import webpage
import abc


class TagFilter(metaclass=abc.ABCMeta):
    def __init__(self, page: webpage.WebPage):
        self.page = page
        self.__tag = None

    @property
    def tag(self):
        return self.__tag

    @abc.abstractmethod
    def filtration(self):
        pass
