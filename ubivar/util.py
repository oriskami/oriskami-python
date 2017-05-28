from __future__ import print_function

import hmac
import logging
import sys
import os
import re

import ubivar


UBIVAR_LOG = os.environ.get('UBIVAR_LOG')

logger = logging.getLogger('ubivar')

__all__ = [
    'StringIO',
    'parse_qsl',
    'json',
    'utf8',
    'log_info',
    'log_debug',
    'dashboard_link',
    'logfmt',
]

try:
    # When cStringIO is available
    import cStringIO as StringIO
except ImportError:
    from io import StringIO

try:
    from urllib.parse import parse_sql
except ImportError:
    # Python < 2.6
    from cgi import parse_qsl

try:
    import json
except ImportError:
    json = None

if not (json and hasattr(json, 'loads')):
    try:
        import simplejson as json
    except ImportError:
        if not json:
            raise ImportError(
                "Ubivar requires a JSON library, such as simplejson. "
                "HINT: Try installing the "
                "python simplejson library via 'pip install simplejson' or "
                "'easy_install simplejson', or contact support@ubivar.com "
                "with questions.")
        else:
            raise ImportError(
                "Ubivar requires a JSON library with the same interface as "
                "the Python 2.6 'json' library.  You appear to have a 'json' "
                "library with a different interface.  Please install "
                "the simplejson library.  HINT: Try installing the "
                "python simplejson library via 'pip install simplejson' "
                "or 'easy_install simplejson', or contact support@ubivar.com"
                "with questions.")


def utf8(value):
    # Note the ordering of these conditionals: `unicode` isn't a symbol in
    # Python 3 so make sure to check version before trying to use it. Python
    # 2to3 will also boil out `unicode`.
    if sys.version_info < (3, 0) and isinstance(value, unicode):
        return value.encode('utf-8')
    else:
        return value


def is_appengine_dev():
    return ('APPENGINE_RUNTIME' in os.environ and
            'Dev' in os.environ.get('SERVER_SOFTWARE', ''))


def _console_log_level():
    if ubivar.log in ['debug', 'info']:
        return ubivar.log
    elif UBIVAR_LOG in ['debug', 'info']:
        return UBIVAR_LOG
    else:
        return None


def log_debug(message, **params):
    msg = logfmt(dict(message=message, **params))
    if _console_log_level() == 'debug':
        print(msg, file=sys.stderr)
    logger.debug(msg)


def log_info(message, **params):
    msg = logfmt(dict(message=message, **params))
    if _console_log_level() in ['debug', 'info']:
        print(msg, file=sys.stderr)
    logger.info(msg)


def _test_or_live_environment():
    if ubivar.api_key is None:
        return
    match = re.match(r'sk_(live|test)_', ubivar.api_key)
    if match is None:
        return
    return match.groups()[0]


def dashboard_link(request_id):
    return 'https://dashboard.ubivar.com/{env}/logs/{reqid}'.format(
        env=_test_or_live_environment() or 'test',
        reqid=request_id,
    )


def logfmt(props):
    def fmt(key, val):
        # Check if val is already a string to avoid re-encoding into
        # ascii. Since the code is sent through 2to3, we can't just
        # use unicode(val, encoding='utf8') since it will be
        # translated incorrectly.
        if re.search(r'\s', str(val)):
            val = repr(val)
        # key should already be a string
        if re.search(r'\s', key):
            key = repr(key)
        return u'{key}={val}'.format(key=key, val=val)
    return u' '.join([fmt(key, val) for key, val in sorted(props.items())])


# Borrowed from Django's source code
if hasattr(hmac, 'compare_digest'):
    # Prefer the stdlib implementation, when available.
    def secure_compare(val1, val2):
        return hmac.compare_digest(utf8(val1), utf8(val2))
else:
    def secure_compare(val1, val2):
        """
        Returns True if the two strings are equal, False otherwise.
        The time taken is independent of the number of characters that match.
        For the sake of simplicity, this function executes in constant time
        only when the two strings have the same length. It short-circuits when
        they have different lengths.
        """
        val1, val2 = utf8(val1), utf8(val2)
        if len(val1) != len(val2):
            return False
        result = 0
        if (sys.version_info[0] == 3 and isinstance(val1, bytes) and
                isinstance(val2, bytes)):
            for x, y in zip(val1, val2):
                result |= x ^ y
        else:
            for x, y in zip(val1, val2):
                result |= ord(x) ^ ord(y)
        return result == 0
