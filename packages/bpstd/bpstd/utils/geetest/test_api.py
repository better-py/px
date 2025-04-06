import json

from .geetest import stage_one, stage_two


def test_stage1():
    result = stage_one()
    json.dumps(result)
    print(result)


def test_stage2():
    result = stage_two(
        "f19a50cd513be79a69e70235de039a41",
        "a4e5f64613509f8546a2c73f5958ce48",
        "a4e5f64613509f8546a2c73f5958ce48|jordan",
    )
    print(result)
