from ..utils.sign import generate_sign_sha256, validate_sign_sha256


def test_sign_sha256():
    secret_key = "hello test"
    task = {
        "a": 1,
        "b": 1,
        "c": 1,
        "d": 1,
        "a2": 2,
        "b2": 2,
        "c2": 2,
        "d2": 2,
    }

    sign = generate_sign_sha256(payload=task, secret_key=secret_key)
    print("sign: ", sign)

    is_true = validate_sign_sha256(payload=task, secret_key=secret_key, input_sign=sign)
    assert is_true is True
