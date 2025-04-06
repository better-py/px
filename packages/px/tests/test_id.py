import pytest

import px
from px.id import generate_13_str, generate_19_digit


@pytest.mark.skip("skip")
def test_id():
    ret = px.hello()
    print(f"ret: {ret}")

    for i in range(10):
        id1, id2 = px.generate_18_digit(), px.generate_13_str()

        print(f"{id1}, {id2}, size: {len(str(id1))}, {len(str(id2))}")


def test_snowflake():
    """task t -- tests/test_id.py::test_snowflake"""

    for i in range(10):
        id1, id2 = (
            generate_19_digit(adopter="discord"),
            generate_19_digit(adopter="twitter"),
        )
        id3, id4, id5 = (
            generate_13_str(adopter="discord"),
            generate_13_str(adopter="twitter"),
            generate_13_str(adopter="tsid"),
        )

        print(
            f"snowflake digit id: {id1}, {id2}, size: {len(str(id1))}, {len(str(id2))}"
        )
        print(
            f"snowflake str id: {id3, id4, id5}, size:  {len(str(id3)), len(str(id4)), len(str(id5))}"
        )


def test_benchmark():
    import timeit

    ret = timeit.timeit(
        "px.generate_id_digit()",
        setup="import px",
        number=100000,
    )

    print(f"timeit: {ret}")
    ret = timeit.timeit(
        "px.generate_id_str()",
        setup="import px",
        number=100000,
    )

    print(f"timeit: {ret}")

    # for i in range(100):
    #     px.generate_id_digit()

    # for i in range(100):
    #     px.generate_id_str()
