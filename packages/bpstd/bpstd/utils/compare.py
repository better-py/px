# -*- coding: utf-8 -*-


def compare_intersect(a, b):
    return frozenset(a).issubset(b)
