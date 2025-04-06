import logging

from django.db import connection
from django.utils.deprecation import MiddlewareMixin


logger = logging.getLogger(__name__)


class TerminalLogging(MiddlewareMixin):
    def process_response(self, request, response):
        for query in connection.queries:
            logger.info(
                "\033[1;31m[%s]\033[0m \033[1m%s\033[0m"
                % (query["time"], " ".join(query["sql"].split()))
            )

        return response
