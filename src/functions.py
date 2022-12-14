import copy
import os.path
import json
import ast

from ainfox.dealer.divfilter import DivFilter
from ainfox.dealer.tablefilter import TableFilter
from ainfox.dealer.processor import TableDealer
from ainfox.dealer.analyzer import DivDealer
from ainfox.webpage.webpage import WebPage
from ainfox.matching.manual_word_table import load_word_table, matching

from bs4 import BeautifulSoup


def data_match(json_str):
    data_dict = ast.literal_eval(json_str)
    print(data_dict)
    ret = copy.deepcopy(data_dict)
    word_table = load_word_table()
    for k in data_dict:
        if k == 'Unknown':
            del ret[k]
            continue
        concept = matching(k, word_table)
        ret[concept] = ret.pop(k)
    print("After matching returns:", ret)
    return json.dumps(ret, ensure_ascii=False)


def extraction(_url):
    # url = input("Input a url: ")
    datajson = {}
    changed_url = _url.replace('//', '__').replace('/', '_').replace('.', '-').replace(':', '--')
    base_dir = f'./out/{changed_url}'
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)
    table_dir = os.path.join(base_dir, 'tables')
    if not os.path.exists(os.path.join(table_dir)):
        os.mkdir(table_dir)
    div_dir = os.path.join(base_dir, 'div')
    if not os.path.exists(os.path.join(div_dir)):
        os.mkdir(div_dir)

    page = WebPage(url=_url)
    page.crawl(response_type="get")
    page.analyze()
    # print(page.soup)

    div_filter = DivFilter(page)
    table_filter = TableFilter(page)

    table_dealer = TableDealer()
    div_dealer = DivDealer()

    divs = div_filter.filtration()
    tables = table_filter.filtration()

    datajson = dict()
    # print("Tables below:")
    # print(tables, len(tables))
    # print("Div tags below:")
    # print(divs, len(divs))

    # table
    if not tables:
        print("No table to extract...")
    else:
        for i, table in enumerate(tables):
            print(i, table)
            in_html = str(table)
            in_html = table_dealer.replace_br(in_html)
            in_html = table_dealer.replace_p(in_html)
            print(in_html)
            try:
                in_df = table_dealer.to_table(in_html)
            except ValueError:
                continue
            print(in_df)
            entries = table_dealer.get_entries(in_df)
            # print(entries)
            datajson.update(dict(datajson, **entries))
            path = os.path.join(table_dir, f'table_{i}.json')
            table_dealer.save_as_json(entries, path)

    # div
    if not divs:
        print("Didn't find div tag to extract...")
    else:
        new = div_dealer.normalize(str(divs[0]))
        titles = div_dealer.find_titles(new)
        print(titles)
        if titles[0].name == 'h1':
            datajson.update({'??????': titles[0].text})
            del titles[0]
        soup = BeautifulSoup(new, features="lxml")
        segments = div_dealer.segmentation(soup, titles)
        print(segments)
        entries = div_dealer.get_entries(segments)
        print(entries)
        datajson.update(dict(datajson, **entries))
        path = os.path.join(div_dir, f'div.json')
        div_dealer.save_as_json(entries, path)
        ret = copy.deepcopy(datajson)
        for k, v in datajson.items():
            if type(v) != list:
                ret[k] = [v]
    return json.dumps(ret, ensure_ascii=False)


if __name__ == '__main__':
    url = input()
    # extraction()
