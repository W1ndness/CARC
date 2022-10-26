# -*- coding: utf-8 -*-
import json
import re
from typing import Union, Any

import pandas as pd


class TableDealer:
    @staticmethod
    def to_table(table_tag: str):
        return pd.read_html(table_tag, encoding='utf-8', header=0)[0]

    @staticmethod
    def replace_br(table_tag: str, replace_with='_._br_._'):
        table_tag = table_tag.replace('<br>', replace_with)
        return table_tag

    @staticmethod
    def replace_p(table_tag: str, replace_with='_._p_._'):
        table_tag = table_tag.replace('<p>', '')
        table_tag = table_tag.replace('</p>', replace_with)
        return table_tag

    @staticmethod
    def dropna(table_df: pd.DataFrame):
        table_df.dropna(axis=1, inplace=True, how='all')
        table_df.dropna(inplace=True, how='all')
        return table_df

    @staticmethod
    def rename_headers(table_df: pd.DataFrame):
        def is2columns():
            if len(table_df.columns) != 2:
                raise TableColumnException(len(table_df.columns))

        try:
            is2columns()
        except TableColumnException as e:
            print("The table doesn't have two columns. It cannot be renamed.")
        else:
            table_df.columns = ['key', 'value']

        return table_df

    @staticmethod
    def get_entries(table_df: pd.DataFrame):
        dealer = TableDealer()
        dealer.dropna(table_df)
        if list(table_df.columns) != ['key', 'value']:
            dealer.rename_headers(table_df)

        _entries: dict[str, list[Union[str, Any]]] = {}
        for index, row in table_df.iterrows():
            key, value = str(row['key']), str(row['value'])
            key = key.strip()
            key = key.replace(':', '')
            key = key.replace('：', '')
            key = key.replace('_._br_._', '')
            value = value.replace('_._br_._', '\n')
            value = value.replace('_._p_._', '\n')
            val = list(value.split('\n'))
            if len(val) == 1:
                if any([each in value for each in ['。', ';']]):
                    val = re.split('。|;', value)
                else:
                    val = re.split('、|,|，', value)
            if val[-1] == "":
                del val[-1]
            if len(val) == 1:
                val = re.split('、|,|，', value)
            val = [each.strip() for each in val]

            # val = list(value.split(['\n', ',', '、', ';', '，']))
            # if len(val) == 1:
            #     val = list(value.split([',']))
            _entries.update({key: val})
        return _entries

    @staticmethod
    def save_as_json(_entries, path):
        with open(path, 'w', encoding='utf-8') as fp:
            fp.write(json.dumps(_entries, ensure_ascii=False, indent=4))


class TableColumnException(Exception):
    def __init__(self, column_count):
        self.column_count = column_count
