# -*- coding: utf-8 -*-


class DisableCSRFMiddleware(object):
    """DEBUG 模式下, 禁用 csrf 检查:

    - 默认禁用 csrf中间件, 是不够的, SessionAuthentication() 有自己的 csrf 检查.
    - 需要在请求中, 强制不检查

    ref: https://stackoverflow.com/questions/16458166/how-to-disable-djangos-csrf-validation/30639221


    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)
        response = self.get_response(request)
        return response
