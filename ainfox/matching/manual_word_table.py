import ast
import copy
import json
import pkgutil


def load_word_table(path: str = 'word_table.json'):
    """
    Load in the word table.
    :param path: the path of word table, in <.json> format
    :return: the word table as dict
    """
    _word_table = None
    if path != 'word_table.json':
        with open(path, 'r', encoding='utf-8') as _fp:
            _word_table = json.load(_fp)
    else:
        data_bytes = pkgutil.get_data(__package__, 'word_table.json')
        data_str = data_bytes.decode()
        _word_table = ast.literal_eval(data_str)
    return _word_table


def matching(key_str: str, _word_table: dict):
    """
    Search a similar matching for param<key_str> in word table.
    :param key_str: the key to search
    :param _word_table: the word table as dict
    :return: one key in word table if finding successfully, else ask which key to join.
    """
    ret_key = None
    # can find key in word table
    # as original key
    for _key in _word_table:
        if key_str == _key:
            ret_key = _key
    # as other expression of some key
    if ret_key is None:
        for _key, values in _word_table.items():
            for value in values:
                # print(f"Now matching {key_str} - {value}")
                if key_str in value or value in key_str:
                    print(f"Find {key_str} as {_key}")
                    ret_key = _key

    # cannot find
    if ret_key is None:
        updated = copy.deepcopy(_word_table)
        print(f"{key_str} cannot find a similar key in word table.")
        new_path = input("New json path?: ")
        for _key in _word_table.keys():
            isvalid = input(f"{key_str} as {_key}? (Y/N): ")
            if isvalid == 'Y':
                updated[_key].append(key_str)
                ret_key = _key
                break
        with open(new_path, 'w') as _fp:
            json.dump(updated, _fp, indent=4)
    return ret_key


if __name__ == '__main__':
    word_table = load_word_table("word_table.json")
    print(word_table)
    with open("../../out/https--__ccst-jlu-edu-cn_info_1322_15733-htm/tables/table_1.json") as fp:
        json_in = json.load(fp)
    for key in json_in.keys():
        matching(key, word_table)
