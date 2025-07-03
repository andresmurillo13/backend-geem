import logging

from security.settings import NAME_LOG
from security.controllers import IpRequest


def log_debug(message, **kwargs):
    logger = logging.getLogger(NAME_LOG)
    extra = kwargs.get('extra') or {}
    request = IpRequest()
    extra['ip'] = request.get_ip()
    logger.debug(message, extra=extra)
