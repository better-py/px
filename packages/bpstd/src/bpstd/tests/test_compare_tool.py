# -*- coding: utf-8 -*-
# @CreateDatetime    :2018/3/15:10:48
# @Author            :Helen
# @Product           :exchange-server
# @Description       : just assert the performance report regarding the frozenset func IT's QUICK GOOD than for loop!
from ..utils.decorator.testutil import func_performance


@func_performance
def test_compare_intersect():
    a = [1, 2, 3]
    b = [2, 1, 3]
    result = frozenset(a).issubset(b)
    assert result == True
