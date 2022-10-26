import os.path
import re

import bs4
from bs4 import BeautifulSoup
import requests

from domnode import Node


class WebPage:
    def __init__(self, **kwargs):
        """
        Constructor
        :param kwargs: information of a web page
        """
        self.url = ""
        self.class_ = "unknown"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/96.0.4664.45 Safari/537.36 "
        }
        self.encoding = 'utf-8'

        self.soup: bs4.BeautifulSoup = None
        self._src = ""
        self._response = None
        self.response_type = None

        if 'url' in kwargs.keys():
            self.url = kwargs['url']
        else:
            raise Exception("The URL is missing from the parameter. Cannot do instantiation.")
        if 'class_' in kwargs.keys():
            self.class_ = kwargs['class_']
        if 'headers' in kwargs.keys():
            self.headers = kwargs['headers']
        if 'encoding' in kwargs.keys():
            self.encoding = kwargs['encoding']

        self.nodes = []
        self.children = []
        self.navigable_strings = []

    @property
    def src_path(self):
        return self._src

    @property
    def response(self):
        return self._response

    def crawl(self, response_type, params=None):
        """
        Crawl src_path from websites.
        :param response_type: ready for requests.xxx
        :param params: ready for requests.post()
        :return: no return
        """
        if self.url == "":
            raise Exception("Haven't got url of the website.")

        self.response_type = response_type

        if response_type not in ["get", "post"]:
            raise Exception("Wrong response type.")

        # get response from url
        if response_type == "get":
            self._response = requests.get(url=self.url, headers=self.headers)
        if response_type == "post":
            if params is None:
                raise Exception("No params.")
            self._response = requests.post(url=self.url, headers=self.headers, params=params)
        self._response.encoding = 'utf-8'

    def save(self, prettier=True):
        """
        Save the src into html file.
        :param prettier: if save prettier
        :return: no return
        """
        # judge if directory which stores src_path of websites exists
        if not os.path.exists("./websites"):
            os.mkdir("./websites")
        if not os.path.exists(f"./websites/{self.class_}"):
            os.mkdir(f"./websites/{self.class_}")
        base_path = f"./websites/{self.class_}"

        # get src_path from response or soup.prettify()
        if not prettier:
            text = self._response.text
        else:
            if self.soup is None:
                raise Exception("Haven't analyze the website.")
            text = self.soup.prettify()

        # generate the string of path and save into the html file
        changed_url = re.sub(r'https://', "", self.url)
        changed_url = re.sub(r'http://', "", changed_url)
        changed_url = changed_url.replace('.', "__")
        changed_url = changed_url.replace('/', '_')
        filename = os.path.join(base_path, changed_url)
        self._src = filename + "-src.html"
        # if os.path.exists(self.src_path):
        #     print(self._src, "already exists.")
        #     return
        with open(self.src_path, 'w', encoding='utf-8') as fp:
            fp.write(text)
        print("Successfully write into", self._src)

    def analyze(self, parser='lxml'):
        """
        Generate a soup instance for the website
        :param parser: parser using in instantiation
        :return: no return
        """
        if self.url == "":
            raise Exception("Haven't got url of the website.")
        if self.response is None:
            raise Exception("Haven't got response from the website.")
        text = self.response.text
        self.soup = BeautifulSoup(text, parser)

    def traverse(self, func):
        """
        traverse the website DOM structures as pre-order
        :param func: operation done on a node
        :return: no return
        """
        self.__dfs(func)

    def __dfs(self, func):
        """
        operation do by function<traverse>, do by soup.descendants
        :param func: operation
        :return: no return
        """
        for child in self.soup.descendants:
            func(child)

    def construct(self, from_head=False):
        """
        construct two lists for nodes and children of nodes which belongs to DOM
        :return: no return
        """
        if self.soup is None:
            raise Exception("Haven't analyze the website.")
        if from_head:
            start = self.soup.contents[0]
        else:
            start = self.soup.body
        for child in start.descendants:
            node = Node(child)
            self.nodes.append(node)
            if isinstance(child, bs4.element.NavigableString):
                self.navigable_strings.append(child)
            self.children.append(node.getChildren())

    def display(self):
        """
        Display structure of the website
        :return: no return
        """
        if self.soup is None:
            raise Exception("Haven't analyze the website.")
        print(self.soup.prettify())
