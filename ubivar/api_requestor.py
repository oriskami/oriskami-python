import calendar
import datetime
import platform
import time
import urllib
from urllib import parse

import ubivar
from ubivar import error, http_client, version, util


def _encode_datetime(dttime):
    if dttime.tzinfo and dttime.tzinfo.utcoffset(dttime) is not None:
        utc_timestamp = calendar.timegm(dttime.utctimetuple())
    else:
        utc_timestamp = time.mktime(dttime.timetuple())

    return int(utc_timestamp)


def _encode_nested_dict(key, data, fmt='%s[%s]'):
    d = {}
    for subkey, subvalue in data.items():
        d[fmt % (key, subkey)] = subvalue
    return d


def _api_encode(data):
    for key, value in data.items():
        key = util.utf8(key)
        if value is None:
            continue
        elif hasattr(value, 'ubivar_id'):
            yield (key, value.ubivar_id)
        elif isinstance(value, list) or isinstance(value, tuple):
            for sv in value:
                if isinstance(sv, dict):
                    subdict = _encode_nested_dict(key, sv, fmt='%s[][%s]')
                    for k, v in _api_encode(subdict):
                        yield (k, v)
                else:
                    yield ("%s[]" % (key,), util.utf8(sv))
        elif isinstance(value, dict):
            subdict = _encode_nested_dict(key, value)
            for subkey, subvalue in _api_encode(subdict):
                yield (subkey, subvalue)
        elif isinstance(value, datetime.datetime):
            yield (key, _encode_datetime(value))
        else:
            yield (key, util.utf8(value))


def _build_api_url(url, query):
    scheme, netloc, path, base_query, fragment = parse.urlsplit(url)

    if base_query:
        query = '%s&%s' % (base_query, query)

    return parse.urlunsplit((scheme, netloc, path, query, fragment))


class APIRequestor(object):

    def __init__(self, key=None, client=None, api_base=None, api_version=None):
        self.api_base = api_base or ubivar.api_base
        self.api_key = key
        self.api_version = api_version or ubivar.api_version

        from ubivar import verify_ssl_certs as verify

        self._client = client or ubivar.default_http_client or \
            http_client.new_default_http_client(
                verify_ssl_certs=verify)

    @classmethod
    def format_app_info(cls, info):
        str = info['name']
        if info['version']:
            str += "/%s" % (info['version'],)
        if info['url']:
            str += " (%s)" % (info['url'],)
        return str

    def request(self, method, url, params=None, headers=None):
        rbody, rcode, rheaders, my_api_key = self.request_raw(
            method.lower(), url, params, headers)
        resp = self.interpret_response(rbody, rcode, rheaders)
        return resp, my_api_key

    def handle_api_error(self, rbody, rcode, resp, rheaders):
        try:
            err = resp['error']
        except (KeyError, TypeError):
            raise error.APIError(
                "Invalid response object from API: %r (HTTP response code "
                "was %d)" % (rbody, rcode),
                rbody, rcode, resp)

        # Rate limits were previously coded as 400's with code 'rate_limit'
        if rcode == 429 or (rcode == 400 and err.get('code') == 'rate_limit'):
            raise error.RateLimitError(
                err.get('message'), rbody, rcode, resp, rheaders)
        elif rcode in [400, 404]:
            raise error.InvalidRequestError(
                err.get('message'), err.get('param'),
                rbody, rcode, resp, rheaders)
        elif rcode == 401:
            raise error.AuthenticationError(
                err.get('message'), rbody, rcode, resp,
                rheaders)
        elif rcode == 402:
            raise error.CardError(err.get('message'), err.get('param'),
                                  err.get('code'), rbody, rcode, resp,
                                  rheaders)
        elif rcode == 403:
            raise error.PermissionError(
                err.get('message'), rbody, rcode, resp,
                rheaders)
        else:
            raise error.APIError(err.get('message'), rbody, rcode, resp,
                                 rheaders)

    def request_headers(self, api_key, method):
        user_agent = 'Ubivar/v1 PythonBindings/%s' % (version.VERSION,)
        if ubivar.app_info:
            user_agent += " " + self.format_app_info(ubivar.app_info)

        ua = {
            'bindings_version': version.VERSION,
            'lang': 'python',
            'publisher': 'ubivar',
            'httplib': self._client.name,
        }
        for attr, func in [['lang_version', platform.python_version],
                           ['platform', platform.platform],
                           ['uname', lambda: ' '.join(platform.uname())]]:
            try:
                val = func()
            except Exception as e:
                val = "!! %s" % (e,)
            ua[attr] = val
        if ubivar.app_info:
            ua['application'] = ubivar.app_info

        headers = {
            'X-Ubivar-Client-User-Agent': util.json.dumps(ua),
            'User-Agent': user_agent,
            'Authorization': 'Bearer %s' % (api_key,),
        }

        if method == 'post':
            headers['Content-Type'] = 'application/x-www-form-urlencoded'

        if self.api_version is not None:
            headers['Accept-version'] = self.api_version

        return headers

    def request_raw(self, method, url, params=None, supplied_headers=None):
        """
        Mechanism for issuing an API call
        """

        if self.api_key:
            my_api_key = self.api_key
        else:
            from ubivar import api_key
            my_api_key = api_key

        if my_api_key is None:
            raise error.AuthenticationError(
                'No API key provided. (HINT: set your API key using '
                '"ubivar.api_key = <API-KEY>"). You can generate API keys '
                'from the Ubivar web interface.  See https://ubivar.com/api '
                'for details, or email support@ubivar.com if you have any '
                'questions.')

        abs_url = '%s%s' % (self.api_base, url)

        nonenc_api_params = list(_api_encode(params or {}))
        encoded_params = urllib.parse.urlencode(nonenc_api_params)

        if method == 'get' or method == 'delete':
            if params:
                abs_url = _build_api_url(abs_url, encoded_params)
            post_data = None
        elif method == 'post':
            post_data = encoded_params
        else:
            raise error.APIConnectionError(
                'Unrecognized HTTP method %r.  This may indicate a bug in the '
                'Ubivar bindings.  Please contact support@ubivar.com for '
                'assistance.' % (method,))

        headers = self.request_headers(my_api_key, method)

        if supplied_headers is not None:
            for key, value in supplied_headers.items():
                headers[key] = value

        util.log_info('Request to Ubivar api', method=method, path=abs_url)
        util.log_debug(
            'Post details', post_data=post_data, api_version=self.api_version)

        rbody, rcode, rheaders = self._client.request(
            method, abs_url, headers, post_data)

        util.log_info(
            'Ubivar API response', path=abs_url, response_code=rcode)
        util.log_debug('API response body', body=rbody)
        if 'Request-Id' in rheaders:
            util.log_debug('Dashboard link for request',
                           link=util.dashboard_link(rheaders['Request-Id']))
        return rbody, rcode, rheaders, my_api_key

    def interpret_response(self, rbody, rcode, rheaders):
        try:
            if hasattr(rbody, 'decode'):
                rbody = rbody.decode('utf-8')
            resp = util.json.loads(rbody)
        except Exception:
            raise error.APIError(
                "Invalid response body from API: %s "
                "(HTTP response code was %d)" % (rbody, rcode),
                rbody, rcode, rheaders)
        if not (200 <= rcode < 300):
            util.log_info(
                'Ubivar API error received',
                error_code=resp.get('error', {}).get('code'),
                error_type=resp.get('error', {}).get('type'),
                error_message=resp.get('error', {}).get('message'),
                error_param=resp.get('error', {}).get('param'),
            )
            self.handle_api_error(rbody, rcode, resp, rheaders)
        return resp
