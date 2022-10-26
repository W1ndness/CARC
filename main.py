import os.path

from dealer.divfilter import DivFilter
from dealer.tablefilter import TableFilter
from dealer.processor import TableDealer
from dealer.analyzer import DivDealer
from webpage import WebPage

from bs4 import BeautifulSoup


def extraction():
    url = input("Input a url: ")

    changed_url = url.replace('//', '__').replace('/', '_').replace('.', '-').replace(':', '--')
    base_dir = f'./out/{changed_url}'
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)
    table_dir = os.path.join(base_dir, 'tables')
    if not os.path.exists(os.path.join(table_dir)):
        os.mkdir(table_dir)
    div_dir = os.path.join(base_dir, 'div')
    if not os.path.exists(os.path.join(div_dir)):
        os.mkdir(div_dir)

    page = WebPage(url=url)
    page.crawl(response_type="get")
    page.analyze()

    div_filter = DivFilter(page)
    table_filter = TableFilter(page)
    table_dealer = TableDealer()
    div_dealer = DivDealer()

    divs = div_filter.filtration()
    tables = table_filter.filtration()

    # table
    if not tables:
        pass
    else:
        for i, table in enumerate(tables):
            in_html = str(table)
            in_html = table_dealer.replace_br(in_html)
            in_html = table_dealer.replace_p(in_html)
            in_df = table_dealer.to_table(in_html)
            entries = table_dealer.get_entries(in_df)
            path = os.path.join(table_dir, f'table_{i}.json')
            table_dealer.save_as_json(entries, path)

    # div
    if not divs:
        pass
    elif tables:
        pass
    else:
        new = div_dealer.normalize(str(divs[0]))
        titles = div_dealer.find_titles(new)
        soup = BeautifulSoup(new, features="lxml")
        segments = div_dealer.segmentation(soup, titles)
        entries = div_dealer.get_entries(segments)
        path = os.path.join(div_dir, f'div.json')
        div_dealer.save_as_json(entries, path)


def matching():



if __name__ == '__main__':
    extraction()
    matching()
