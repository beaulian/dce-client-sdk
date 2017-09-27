# coding=utf-8

from ..utils import (
    camelize_dict, check_bool_str,
    wrapper_check_resource
)


class ExtensionAPiMixin:
    def read_extensions_router(self, extended_point=None):
        url = '/extensions/{0}'.format(extended_point)

        return self._result(self._get(self._url(url)), json=True)


class PluginApiMixin(ExtensionAPiMixin):
    def list_plugin(self, categories=None, is_enabled='False',
                    builtin_only='False', iter=False, limit=None):
        check_bool_str(is_enabled=is_enabled, builtin_only=builtin_only)

        url = '/plugins'
        params = camelize_dict({
            'categories': categories or [],
            'is_enabled': is_enabled,
            'builtin_only': builtin_only
        })

        if iter or limit:
            return self._advanced_result(self._advanced_get(self._url(url), params=params),
                                         iter=iter, limit=limit, json=True)
        else:
            return self._result(self._get(self._url(url), params=params),
                                json=True)

    def create_plugin(self, image=None, auth=None, is_enabled=None):
        check_bool_str(is_enabled=is_enabled)

        url = '/plugins'
        data = camelize_dict({
            'image': image,
            'auth': auth or {},
            'is_enabled': is_enabled
        })

        return self._result(self._post(self._url(url), json=data))

    def read_plugin(self, plugin):
        url = '/plugins/{0}'.format(plugin)

        return self._result(self._get(self._url(url)), json=True)

    def delete_plugin(self, plugin):
        url = '/plugins/{0}'.format(plugin)

        return self._result(self._delete(self._url(url)))

    def validate_plugin(self, image=None, auth=None):
        url = '/plugins-utils/validate'
        data = camelize_dict({
            'image': image,
            'auth': auth or {}
        })

        return self._result(self._post(self._url(url), json=data))

    def enable_plugin(self, plugin):
        url = '/plugins/{0}/enable'.format(plugin)

        return self._result(self._post(self._url(url)))

    def disable_plugin(self, plugin):
        url = '/plugins/{0}/disable'.format(plugin)

        return self._result(self._post(self._url(url)))

    def upgrade_plugin(self, plugin, image=None, auth=None):
        url = '/plugins/{0}/upgrade'.format(plugin)
        data = camelize_dict({
            'image': image,
            'auth': auth or {}
        })

        return self._result(self._post(self._url(url), json=data))

    def validate_builtin_plugin_context(self, plugin):
        url = '/builtin-plugins/{0}/validate'.format(plugin)

        return self._result(self._post(self._url(url)))

    def read_builtin_plugin_context(self, plugin):
        url = '/builtin-plugins/{0}/settings'.format(plugin)

        return self._result(self._get(self._url(url)), json=True)

    def save_builtin_plugin_context(self, plugin, **kwargs):
        url = '/builtin-plugins/{0}/settings'.format(plugin)

        return self._result(self._post(self._url(url), json=kwargs))

    def read_external_plugin_context(self, plugin):
        url = '/plugins-storage/{0}/config'.format(plugin)

        return self._result(self._get(self._url(url)), json=True)

    def save_external_plugin_context(self, plugin, **kwargs):
        url = '/plugins-storage/{0}/config'.format(plugin)

        return self._result(self._put(self._url(url), json=kwargs))

    def list_plugin_storage_catalog(self, iter=False, limit=None):
        url = '/plugin-store/catalog'

        if iter or limit:
            return self._advanced_result(self._advanced_get(self._url(url)),
                                         iter=iter, limit=limit, json=True)
        else:
            return self._result(self._get(self._url(url)), json=True)

    def read_from_plugin_storage(self, plugin):
        url = '/plugin-store/{0}'.format(plugin)

        return self._result(self._get(self._url(url)), json=True)

    def list_plugin_job(self, plugin, iter=False, limit=None):
        url = '/plugins-utils/{0}/jobs'.format(plugin)

        if iter or limit:
            return self._advanced_result(self._advanced_get(self._url(url)),
                                         iter=iter, limit=limit, json=True)
        else:
            return self._result(self._get(self._url(url)), json=True)

    def create_plugin_job(self, plugin, name=None, reason=None,
                          state=None, extra_context=None):
        url = '/plugins-utils/{0}/jobs'.format(plugin)
        data = camelize_dict({
            'name': name,
            'reason': reason or {},
            'state': state,
            'extra_context': extra_context or {}
        })

        return self._result(self._post(self._url(url), json=data))


wrapper_check_resource(PluginApiMixin)
