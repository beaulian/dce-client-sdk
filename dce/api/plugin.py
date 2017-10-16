# coding=utf-8

from ..utils import (
    camelize_dict, check_bool_str,
    wrap_checking_resource
)


class PluginApiMixin:
    def list_plugin(self, categories=None, is_enabled='False',
                    builtin_only='False', iter=False, limit=None):
        """
        Get plugins.

        :param categories: the categories of plugin, exact match。
        :param is_enabled: is enabled or not, boolean string.
        :param builtin_only: is builtin only or not, boolean string.
        :param iter: if `True`, return a generator of plugins.
        :param limit: the number of plugins allowed to return
                      if None, return all plugins.

        :return: a list of dicts, one per plugin.

        :raise ValueError: if `is_enabled` or `builtin_only` is neither
                           a boolean string nor None.
        :raise TypeError: if `limit` is neither a integer nor None.
        :raise APIError: if server returns an error.
        """
        check_bool_str(is_enabled=is_enabled, builtin_only=builtin_only)

        url = '/plugins'
        params = camelize_dict({
            'categories': categories or [],
            'is_enabled': is_enabled,
            'builtin_only': builtin_only
        })

        if iter or limit:
            return self._advanced_result(
                self._advanced_get(self._url(url), params=params),
                iter=iter, limit=limit, json=True
            )
        else:
            return self._result(
                self._get(self._url(url), params=params), json=True
            )

    def create_plugin(self, image=None, auth=None, is_enabled=None):
        """
        Create plugin.

        :param image: the image uri.
        :param auth: a dict including `username` and `password`,
                     if pulling image requires authentication, `username`
                     and `password` are required.
        :param is_enabled: is enabled or not, boolean string.

        :return: the plugin.

        :raise ValueError: if `is_enabled` is neither a boolean string nor None.
        :raise APIError: if server returns an error.
        """
        check_bool_str(is_enabled=is_enabled)

        url = '/plugins'
        data = camelize_dict({
            'image': image,
            'auth': auth or {},
            'is_enabled': is_enabled
        })

        return self._result(
            self._post(self._url(url), json=data), json=True
        )

    def read_plugin(self, plugin):
        """
        Read plugin's detail.

        :param plugin: the name of plugin.

        :return: the plugin.

        :raise APIError: if server returns an error.
        """
        url = '/plugins/{0}'.format(plugin)

        return self._result(self._get(self._url(url)), json=True)

    def delete_plugin(self, plugin):
        """
        Delete plugin.

        :param plugin: the name of plugin.

        :raise APIError: if server returns an error.
        """
        url = '/plugins/{0}'.format(plugin)

        res = self._delete(self._url(url))
        self._raise_for_status(res)

    def validate_plugin(self, image=None, auth=None):
        """
        Validate plugin.

        :param image: the image uri.
        :param auth: a dict including `username` and `password`,
                     if pulling image requires authentication, `username`
                     and `password` are required.

        :return: the plugin.

        :raise APIError: if server returns an error.
        """
        url = '/plugins-utils/validate'
        data = camelize_dict({
            'image': image,
            'auth': auth or {}
        })

        return self._result(
            self._post(self._url(url), json=data), json=True
        )

    def enable_plugin(self, plugin):
        """
        Enable plugin.

        :param plugin: the name of plugin.

        :return: the plugin.

        :raise APIError: if server returns an error.
        """
        url = '/plugins/{0}/enable'.format(plugin)

        return self._result(self._post(self._url(url)), json=True)

    def disable_plugin(self, plugin):
        """
        Disable plugin.

        :param plugin: the name of plugin.

        :return: the plugin.

        :raise APIError: if server returns an error.
        """
        url = '/plugins/{0}/disable'.format(plugin)

        return self._result(self._post(self._url(url)), json=True)

    def upgrade_plugin(self, plugin, image=None, auth=None):
        """
        Upgrade plugin.

        :param plugin: the name of plugin.
        :param image: the image uri.
        :param auth: a dict including `username` and `password`,
                     if pulling image requires authentication, `username`
                     and `password` are required.

        :return: the plugin.

        :raise APIError: if server returns an error.
        """
        url = '/plugins/{0}/upgrade'.format(plugin)
        data = camelize_dict({
            'image': image,
            'auth': auth or {}
        })

        return self._result(
            self._post(self._url(url), json=data), json=True
        )

    def validate_builtin_plugin_config(self, plugin, **kwargs):
        """
        Validate builtin plugin's config.

        :param plugin: the name of plugin.
        :param kwargs: the extra params if need,
                       the builtin plugins are Lenovo-UUS, DockerRegistry,
                       ScaleIO, vSphere, DaoCloud, OpenStack, AWS-EC2,
                       for Lenovo-UUS, kwargs include:
                            `endpoint`, `username`, `password`
                       for DockerRegistry, kwargs include:
                            `registry_address`, `username`, `password`, `verify_ssl`
                       for ScaleIO, kwargs include:
                            `endpoint`, `username`, `password`, `system_name`,
                            `storage_pool_name`, `Protection_domain_name`,
                            `insecure`, `mdm_master_ip`
                       for vSphere, kwargs include:
                            `vcenter`, `username`, `password`
                       for DaoCloud, kwargs include:
                            `username`, `password`, `email`
                       for OpenStack, kwargs include:
                            `username`, `password`, `auth_url`, `tenant_name`,
                            `region`, `api_endpoint`
                       for AWS-EC2, kwargs include:
                            `region`, `api_key`, `api_secret`.

        :return: the integration information of plugin.

        :raise APIError: if server returns an error.
        """
        url = '/builtin-plugins/{0}/validate'.format(plugin)

        return self._result(
            self._post(self._url(url), json=camelize_dict(kwargs)),
            json=True
        )

    def read_builtin_plugin_config(self, plugin):
        """
        Read builtin plugin's config.

        :param plugin: the name of plugin.

        :return: the builtin plugin's config.

        :raise APIError: if server returns an error.
        """
        url = '/builtin-plugins/{0}/settings'.format(plugin)

        return self._result(self._get(self._url(url)), json=True)

    def save_builtin_plugin_config(self, plugin, config):
        """
        Save builtin plugin's config.

        :param plugin: the name of plugin.
        :param config: the config that is will saved, dict.

        :return: the builtin plugin's config.

        :raise APIError: if server returns an error.
        """
        url = '/builtin-plugins/{0}/settings'.format(plugin)

        return self._result(
            self._post(self._url(url), json=config), json=True
        )

    def read_external_plugin_config(self, plugin):
        """
        Read external plugin's config.

        :param plugin: the name of plugin.

        :return: the external plugin's config.

        :raise APIError: if server returns an error.
        """
        url = '/plugins-storage/{0}/config'.format(plugin)

        return self._result(self._get(self._url(url)), json=True)

    def save_external_plugin_config(self, plugin, config):
        """
        Save external plugin's config.

        :param plugin: the name of plugin.
        :param config: he config that is will saved, dict.

        :return: the external plugin's config.

        :raise APIError: if server returns an error.
        """
        url = '/plugins-storage/{0}/config'.format(plugin)

        return self._result(
            self._put(self._url(url), json=config), json=True
        )

    def list_plugin_storage_catalog(self, iter=False, limit=None):
        """
        Get plugin's storage catalogs.

        :param iter: if `True`, return a generator of catalogs.
        :param limit: the number of catalogs allowed to return
                      if None, return all catalogs.

        :return: a list of dicts, one per catalog.

        :raise TypeError: if `limit` is neither a integer nor None.
        :raise APIError: if server returns an error.
        """
        url = '/plugin-store/catalog'

        if iter or limit:
            return self._advanced_result(self._advanced_get(self._url(url)),
                                         iter=iter, limit=limit, json=True)
        else:
            return self._result(self._get(self._url(url)), json=True)

    def read_plugin_from_plugin_storage(self, plugin):
        """
        Read plugin from plugin storage.

        :param plugin: the name of plugin.

        :return: the plugin.

        :raise APIError: if server returns an error.
        """
        url = '/plugin-store/{0}'.format(plugin)

        return self._result(self._get(self._url(url)), json=True)

    def list_plugin_job(self, plugin, iter=False, limit=None):
        """
        Get plugin's jobs.

        :param plugin: the name of plugin.
        :param iter: if `True`, return a generator of jobs.
        :param limit: the number of jobs allowed to return
                      if None, return all jobs.

        :return: a list of dicts, one per plugin job.

        :raise TypeError: if `limit` is neither a integer nor None.
        :raise APIError: if server returns an error.
        """
        url = '/plugins-utils/{0}/jobs'.format(plugin)

        if iter or limit:
            return self._advanced_result(self._advanced_get(self._url(url)),
                                         iter=iter, limit=limit, json=True)
        else:
            return self._result(self._get(self._url(url)), json=True)

    def create_plugin_job(self, plugin, name=None, reason=None,
                          state=None, extra_context=None):
        """
        Create plugin's job.

        :param plugin: the name of plugin.
        :param name: the name of job.
        :param reason: the reason of running job.
        :param state: the state of job.
        :param extra_context: the extra context of job, dict.

        :return: the plugin's job.

        :raise APIError: if server returns an error.
        """
        url = '/plugins-utils/{0}/jobs'.format(plugin)
        data = camelize_dict({
            'name': name,
            'reason': reason or {},
            'state': state,
            'extra_context': extra_context or {}
        })

        return self._result(
            self._post(self._url(url), json=data), json=True
        )


wrap_checking_resource(PluginApiMixin)
