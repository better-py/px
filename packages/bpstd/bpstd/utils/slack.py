import logging
import os

from slack import WebClient as SlackClient


logger = logging.getLogger(__name__)

# slack bot token:
SLACK_API_TOKEN = os.getenv("SLACK_API_TOKEN", "default slack api token")


def slack_query_user(token, username):
    sc = SlackClient(token)
    resp = sc.api_call("users.list")

    users = resp.get("members")
    for user in users:
        if user["name"] == username or user["profile"]["real_name"] == username:
            # print("match user: {}".format(user))
            msg = "user: {}, real_name: {}, id: {}".format(
                user["name"],
                user["profile"]["real_name"],
                user["id"],
            )
            logger.debug(msg)
            return user["id"]
    return None


def slack_post_message(token, channel, text):
    """
    emoji:  :tada:

    @ slack user format:
        <@U6GQW1ZA7>: <@U2NNHEW21>:
        <@U6GQW1ZA7> <@U2NNHEW21> <@U0EEB0NSC>

    :param token:
    :param channel:
    :param text: msg
    :return:
    """
    sc = SlackClient(token)
    resp = sc.api_call(
        "chat.postMessage",
        channel=channel,
        text=text,
    )
    return resp
