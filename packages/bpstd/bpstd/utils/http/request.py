# -*- encoding:utf-8 -*-
import logging

import requests

logger = logging.getLogger(__name__)


# HTTP: POST
def http_post(url, payload: dict, timeout=3):
    result = {}
    try:
        r = requests.post(url, data=payload, timeout=timeout)
        # logger.info("Engine Response Status Code:  {}".format(r.status_code))
        if r.status_code != 200:
            result.update(
                RC=-500,
                Reason="engine error: can not handle, invalid params.",
            )
            logger.error("Engine Response: {}".format(r.text))
        else:
            result = r.json()
    except TimeoutError as e:
        result.update(
            RC=-499,
            Reason="engine error: rpc timeout.",
        )
        logger.error("Engine Request Timeout: {}".format(e))
    logger.debug("Engine Request Response: {}".format(result))
    return result
