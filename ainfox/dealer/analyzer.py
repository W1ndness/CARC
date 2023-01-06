import json
import re
from typing import Union, List, Dict

import bs4.element
from bs4 import BeautifulSoup
import unicodedata


# re pattern: <h\d><([a-z]+\S*?)>(?P<content>\S+?)</\1></h\d>

class DivDealer:
    @staticmethod
    def to_text(div_tag: Union[bs4.element.Tag, str], seperator="", replace=False):
        if isinstance(div_tag, str):
            origin = BeautifulSoup(div_tag, features="lxml").body.contents[0]
        else:
            origin = div_tag
        text = origin.get_text(separator=seperator)
        return text.replace('\n', '') if replace else text

    @staticmethod
    def as_repr(div_tag: str):
        return repr(div_tag)

    @staticmethod
    def clean_space(div_tag: str):
        return " ".join(re.split(r"\s+", div_tag.strip()))

    @staticmethod
    def replace(div_tag: str):
        div_tag = div_tag.replace('\xa0', '\n')
        return div_tag

    @staticmethod
    def split(div_tag: str):
        print(div_tag)
        div_tag = div_tag.strip()
        ret = div_tag.split('\n')
        ret = [each.strip() for each in ret]
        ret = [each for each in ret if each != '']
        return ret

    @staticmethod
    def to_entries(tokens: List[str]):
        ret = {}
        for i, token in enumerate(tokens):
            lst = re.split(':|：', token)
            print(lst)
            if '' in lst:
                if lst[0] == '':
                    ret[f"Unknown_{i}"] = lst[1]
                else:
                    ret[lst[0]] = f"Unknown_{i}"
            else:
                ret[lst[0]] = lst[1]
        return ret

    @staticmethod
    def divide_by_div(div_tag: Union[str, bs4.element.Tag], is_recursive=False):
        if isinstance(div_tag, str):
            origin = BeautifulSoup(div_tag, features="lxml").body.contents[0]
        else:
            origin = div_tag
        return origin.find_all('div', recursive=is_recursive)

    @staticmethod
    def find_titles(div_tag: Union[str, bs4.element.Tag]):
        if isinstance(div_tag, str):
            origin = BeautifulSoup(div_tag, features="lxml").body.contents[0]
        else:
            origin = div_tag
        title_tags = origin.find_all({"h1", "h2", "h3", "h4", "h5", "h6", "strong"})
        return title_tags

    @staticmethod
    def normalize(div_tag: str):
        def replace_p(matched):
            content = matched.group("content")
            level = matched.group("lvl")
            return f"<h{level}>{content}</h{level}>"

        new_str = re.sub(r"<h(?P<lvl>\d)><(?P<tag>[a-z]+\S*?)>(?P<content>\S+?)</(?P=tag)></h(?P=lvl)>",
                         replace_p, div_tag)
        return new_str

    @staticmethod
    def segmentation(_soup: BeautifulSoup, title_list: List[bs4.element.Tag]):
        root = _soup.body.contents[0]
        _segments = []
        _titles = title_list[:]
        if _titles[0] != root:
            _titles.insert(0, root)

        _titles = [each for each in _titles if each.text != ""]

        for i in range(len(_titles)):
            if i < len(_titles) - 1:
                st, ed = _titles[i], _titles[i + 1]
                content = ""
                cur = st
                while not isinstance(cur, bs4.element.NavigableString):
                    cur = cur.next_element
                cur = cur.next_element
                # print(cur)
                while cur != ed:
                    if isinstance(cur, bs4.element.NavigableString) and cur != '\n':
                        pattern = r'(http|https|ftp)://\S+'
                        if re.match(pattern, cur):
                            temp = cur.replace(':', "<colon>")
                        else:
                            temp = cur
                        # if (cur.previous_element.name == 'a' and cur.previous_element.previous_element.text != cur) \
                        #         or isinstance(cur.previous_element, bs4.element.NavigableString):
                        #     content = content[:-5]
                        print("content:", content)
                        print("temp:", temp)
                        if temp.strip() != '':
                            content += temp.strip() + '<sep>'
                    cur = cur.next_element
                # content = content[:-5]
                if i == 0:
                    segment = {'Header': content}
                else:
                    segment = {st.text: content}
            else:
                st = _titles[i]
                content = ""
                cur = st
                while not isinstance(cur, bs4.element.NavigableString):
                    cur = cur.next_element
                cur = cur.next_element
                while cur:
                    if isinstance(cur, bs4.element.NavigableString) and cur != '\n':
                        pattern = r'(http|https|ftp)://\S+'
                        if re.match(pattern, cur):
                            temp = cur.replace(':', "<colon>")
                        else:
                            temp = cur
                        # if (cur.previous_element.name == 'a' and cur.previous_element.previous_element.text != cur) \
                        #         or isinstance(cur.previous_element, bs4.element.NavigableString):
                        #     content = content[:-5]
                        if temp.strip() != '':
                            content += temp.strip() + '<sep>'
                    cur = cur.next_element
                    # content = content[:-5]
                segment = {st.text: content}
            _segments.append(segment)
        print("Segments:", _segments)
        return _segments

    @staticmethod
    def get_entries(_segments: List[Dict]):
        def repl(txt):
            prefix = txt.group('pre')
            subfix = txt.group('sub')
            return prefix + '<colon>' + subfix

        _entries = {}
        for segment in _segments:
            (key, value), = segment.items()
            if key == "Header":
                contents = value.split('<sep>')
                for content in contents:
                    content_temp = re.sub(r'(?P<pre>(http|https|ftp)):(?P<sub>//\S+)', repl, content)
                    entry_list = re.split(":|：", content_temp)
                    print(entry_list)
                    if len(entry_list) != 2:
                        if ':' in content or '：' in content:
                            k = entry_list[0].replace(':', '').replace('：', '')
                            v = "Unknown"
                        else:
                            k = "Unknown"
                            v = entry_list[0]
                    else:
                        k, v = entry_list
                    v = v.replace("<colon>", ':')
                    _entries.update({k: v})
            else:
                k = key
                v = value.split('<sep>')
                if v[-1] == "":
                    del v[-1]
                if v and v[0] == "":
                    del v[0]
                v = [each.replace("<colon>", ':') for each in v]
                _entries.update({k: v})
        return _entries

    @staticmethod
    def save_as_json(_entries, path):
        with open(path, 'w', encoding='utf-8') as fp:
            fp.write(json.dumps(_entries, ensure_ascii=False, indent=4))

