from ..utils.config_manager import ConfigCenter


def test_config_center():
    c = ConfigCenter()

    cfg = {
        "k1": "v1",
        "k2": "v1",
        "k3": "v1",
        "k4": {"kk1": "vv1", "kk2": "vv2"},
        "k5": "v1",
    }

    for k, v in cfg.items():
        # c.set(k, v)
        print("info: {}: {}, type={}".format(k, c.get(k), type(c.get(k))))

    c.set("prod_cfg", cfg)

    # 查询字典型结构
    result = c.gets("prod_cfg")

    print("result: {}, type={}".format(result, type(result)))

    print(result.get("k4"))
