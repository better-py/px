from maneki.apps.common.utils.db import DBEngine


def test_create_db():
    host = "10.0.20.83"
    port = "13306"
    user = "root"
    password = "root"
    db_name = "t3"

    e = DBEngine(
        host=host,
        port=port,
        user=user,
        password=password,
        db_name=db_name,
    )

    e.create_db()


def test_drop_db():
    host = "10.0.20.83"
    port = "13306"
    user = "root"
    password = "root"
    db_name = "t3"

    e = DBEngine(
        host=host,
        port=port,
        user=user,
        password=password,
        db_name=db_name,
    )

    e.drop_db()
