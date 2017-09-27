# coding=utf-8
import six
import urllib3
from functools import partial
from semantic_version import Version
from requests.auth import HTTPBasicAuth
from cached_property import cached_property

import requests

from .compat import (
    quote_plus, urlparse
)
from ..consts import (
    DEFAULT_TIMEOUT_SECONDS, DEFAULT_USER_AGENT,
    MINIMUM_DCE_VERSION
)
from ..errors import (
    InvalidVersion, create_api_error_from_http_exception
)
from ..utils.decorators import minimum_version
from .advance import AdvancedMethodMixin
from .registry import RegistryApiMixin
from .account import AccountApiMixin
from .plugin import PluginApiMixin

urllib3.disable_warnings()


class APIClient(requests.Session,
                AdvancedMethodMixin,
                RegistryApiMixin,
                AccountApiMixin,
                PluginApiMixin):
    def __init__(self, base_url=None, username=None, password=None,
                 token=None, timeout=DEFAULT_TIMEOUT_SECONDS,
                 user_agent=DEFAULT_USER_AGENT):
        super(APIClient, self).__init__()

        if base_url.endswith('/'):
            base_url = base_url[:-1]
        if not base_url.startswith('http://') or base_url.startswith('https://'):
            base_url = 'http://' + base_url
        self.base_url = base_url

        self.auth = None
        if username and password:
            self.auth = HTTPBasicAuth(username, password)

        self.verify = False
        self.timeout = timeout
        self.host = urlparse(self.base_url).hostname

        self.headers['User-Agent'] = user_agent
        if token:
            self.headers['X-DCE-Access-Token'] = token

        self._prefix, self._versions = self._retrieve_versions_prefix()
        if Version(self.dce_version) < Version(MINIMUM_DCE_VERSION):
            raise InvalidVersion(
                'DCE Version {} < {} is not supported'.format(
                    self.dce_version, MINIMUM_DCE_VERSION)
            )

    def _retrieve_versions_prefix(self):
        prefix = 'dce'
        try:
            versions = self._version(prefix=prefix)
        except Exception:
            prefix = 'api'
            versions = self._version(prefix=prefix)

        return prefix, versions

    def _version(self, prefix='dce'):
        self._prefix = prefix

        return self._result(
                self._get(self._url('/version')), json=True
        )

    @staticmethod
    def _raise_for_status(response):
        """Raises stored :class:`APIError`, if one occurred."""
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise create_api_error_from_http_exception(e)

    def _result(self, response, json=False, binary=False):
        assert not (json and binary)
        self._raise_for_status(response)

        if json:
            return response.json()
        if binary:
            return response.content
        return response.text

    def _set_request_kwargs(self, kwargs):
        kwargs.setdefault('auth', self.auth)
        kwargs.setdefault('headers', self.headers)
        kwargs.setdefault('timeout', self.timeout)

        return kwargs

    def _request(self, method, url, **kwargs):
        return self.request(method, url, **self._set_request_kwargs(kwargs))

    def _post(self, url, **kwargs):
        return self._request('POST', url, **kwargs)

    def _get(self, url, **kwargs):
        return self._request('GET', url, **kwargs)

    def _put(self, url, **kwargs):
        return self._request('PUT', url, **kwargs)

    def _patch(self, url, **kwargs):
        return self._request('PATCH', url, **kwargs)

    def _delete(self, url, **kwargs):
        return self._request('DELETE', url, **kwargs)

    def _url(self, path, *args, **kwargs):
        for arg in args:
            if not isinstance(arg, six.string_types):
                raise ValueError(
                    'Expected a string but found {0} ({1}) '
                    'instead'.format(arg, type(arg))
                )

        quote_f = partial(quote_plus, safe="/:")
        args = [quote_f(arg) for arg in args]

        return '{0}/{1}{2}'.format(
            self.base_url, self._prefix, path.format(*args, **kwargs)
        )

    @cached_property
    def dce_version(self):
        return self._versions.get('DCEVersion')

    @cached_property
    def info(self):
        return self._result(self._get(self._url('/info')), json=True)

    @property
    def cluster_uuid(self):
        return self.info.get('ClusterUuid')

    @property
    def virt_tech(self):
        return self.info.get('VirtTech')

    @property
    def virt_tech_type(self):
        return self.info.get('VirtTechType')

    @property
    def stream_room(self):
        return self.info.get('StreamRoom')

    @property
    @minimum_version('2.7.13')
    def mode(self):
        return self.info.get('Mode')

    @property
    @minimum_version('2.7.13')
    def network_driver(self):
        return self.info.get('NetworkDriver')

    def ping(self):
        return self._result(self._get(self._url('/ping')))

    def now(self):
        return self._result(self._get(self._url('/now')), json=True)

    def __repr__(self):
        return "<DCEClient '%s'>" % self.host

