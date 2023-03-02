# -*- encoding:utf-8 -*-


def dict_value_to_key(src_dic: dict, value):
    """字典 - 由 value 找 key

    :param src_dic:
    :param value:
    :return:
    """
    for k, v in src_dic.items():
        if value == v:
            return k
    return None
