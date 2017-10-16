# coding=utf-8
from ..utils import (
    camelize_dict, check_bool_str,
    wrap_checking_resource
)

# 旧式类，可修改__dict__属性
class RegistryApiMixin:
    def list_registry_namespace(self, registry, iter=False, limit=None):
        """
        Get registry namespaces.

        :param registry: the name of registry.
        :param iter: if `True`, return a generator of registry namespaces.
        :param limit: the number of registry namespaces allowed to return
                      if None, return all registry namespaces.

        :return: a list of dicts, one per registry namespace.

        :raise TypeError: if limit is not an integer or None.
        :raise APIError: if server returns an error.
        """
        url = '/registries/{0}/namespaces'.format(registry)

        if iter or limit:
            return self._advanced_result(self._advanced_get(self._url(url)),
                                         iter=iter, limit=limit, json=True)
        else:
            return self._result(self._get(self._url(url)), json=True)

    def create_registry_namespace(self, registry, name=None):
        """
        Create registry namespace.

        :param registry: the name of registry.
        :param name: the name of namespace.

        :return: the registry namespace.

        :raise APIError: if server returns an error.
        """
        url = '/registries/{0}/namespaces'.format(registry)

        return self._result(
            self._post(self._url(url), json={'Name': name}),
            json=True
        )

    def read_registry_namespace(self, registry, namespace):
        """
        Read the detail of registry namespace.

        :param registry: the name of registry.
        :param namespace: the name of registry namespace.

        :return: the namespace.

        :raise APIError: if server returns an error.
        """
        url = '/registries/{0}/namespaces/{1}'.format(registry, namespace)

        return self._result(self._get(self._url(url)), json=True)

    def patch_registry_namespace(self, registry, namespace,
                                 short_description=None, visibility=None):
        """
        Update registry namespace.

        :param registry: the name of registry.
        :param namespace: the name of registry namespace.
        :param short_description: the short description of registry namespace.
        :param visibility: the visibility of registry namespace, boolean string or None.

        :return: the registry namespace.

        :raise ValueError: if `visibility` is neither a boolean string nor None.
        :raise APIError: if server returns an error.
        """
        if visibility is not None:
            check_bool_str(visibility=visibility)

        url = '/registries/{0}/namespaces/{1}'.format(registry, namespace)
        data = camelize_dict({
            'short_description': short_description,
            'visibility': visibility
        })

        return self._result(
            self._post(self._url(url), json=data), json=True
        )

    def delete_registry_namespace(self, registry, namespace):
        """
        Delete registry namespace.

        :param registry: the name of registry.
        :param namespace: the name of registry namespace.

        :raise APIError: if server returns an error.
        """
        url = '/registries/{0}/namespaces/{1}'.format(registry, namespace)

        res = self._delete(self._url(url))
        self._raise_for_status(res)

    def authorize_team_for_registry_namespace(self, registry, namespace,
                                              team_id=None, role=None):
        """
        Authorize team for registry namespace.

        :param registry: the name of registry.
        :param namespace: the name of registry namespace.
        :param team_id: the id of team.
        :param role: the authorized role: `no_access` or `view_only`
                     or `restricted_control` or `full_control` or `admin`.

        :return: the registry namespace.
        """
        url = '/registries/{0}/namespaces/{1}/accessible-list'.format(registry, namespace)
        data = camelize_dict({
            'team_id': team_id,
            'role': role
        })

        return self._result(
            self._post(self._url(url), json=data), json=True
        )

    def unauthorize_team_from_registry_namespace(self, registry, namespace, team_id=None):
        """
        Cancel team's authorization from registry namespace.

        :param registry: the name of registry.
        :param namespace: the name of registry namespace.
        :param team_id: the id of team.

        :raise APIError: if server returns an error.
        """
        url = '/registries/{0}/namespaces/{1}/accessible-list'.format(registry, namespace)

        res = self._delete(self._url(url), params={'TeamId': team_id})
        self._raise_for_status(res)

    def list_repository_for_all_registry_namespaces(self, registry, with_remote='True',
                                                    iter=False, limit=None):
        """
        Get all registry namespaces' repositories.

        :param registry: the name of registry.
        :param iter: if `True`, return a generator of repositories.
        :param limit: the number of repositories allowed to return
                      if None, return all repositories.

        :return: a list of dicts, one per repository.

        :raise ValueError: if `with_remote` is neither a boolean string nor None.
        :raise TypeError: if `limit` is neither a integer nor None.
        :raise APIError: if server returns an error.
        """
        check_bool_str(with_remote=with_remote)

        url = '/registries/{0}/repositories'.format(registry)
        data = camelize_dict({
            'with_remote': with_remote
        })

        if iter or limit:
            return self._advanced_result(self._advanced_get(self._url(url), params=data),
                                         iter=iter, limit=limit, json=True)
        else:
            return self._result(self._get(self._url(url), params=data),
                                json=True)

    def list_registry_namespaced_repository(self, registry, namespace,
                                            iter=False, limit=None):
        """
        Get the repositories of given registry namespace.

        :param registry: the name of registry.
        :param namespace: the name of registry namespace.
        :param iter: if `True`, return a generator of repositories.
        :param limit: the number of repositories allowed to return
                      if None, return all repositories.

        :return: a list of dicts, one per repository.

        :raise TypeError: if `limit` is neither a integer nor None.
        :raise APIError: if server returns an error.
        """
        url = '/registries/{0}/repositories/{1}'.format(registry, namespace)

        if iter or limit:
            return self._advanced_result(self._advanced_get(self._url(url)),
                                         iter=iter, limit=limit, json=True)
        else:
            return self._result(self._get(self._url(url)), json=True)

    def create_registry_namespaced_repository(self, registry, namespace, repo_name=None,
                                              short_description=None, long_description=None,
                                              labels=None):
        """
        Create repository of given registry namespace.

        :param registry: the name of registry.
        :param namespace: the name of registry namespace.
        :param repo_name: the repository name of registry namespace.
        :param short_description: the short description of repository.
        :param long_description: the long description of repository.
        :param labels: the labels of repository, dict or None.
                       For example:
                            {
                                "io.daocloud.dce.icon": "name=Python"
                            }

        :return: the repository.

        :raise APIError: if server returns an error.
        """
        url = '/registries/{0}/repositories/{1}'.format(registry, namespace)

        data = camelize_dict({
            'repo_name': repo_name,
            'short_description': short_description,
            'long_description': long_description,
            'labels': labels or {}
        })

        return self._result(
            self._post(self._url(url), json=data), json=True
        )

    def read_registry_namespaced_repository(self, registry, namespace, repository):
        """
        Read repository of given registry namespace.

        :param registry: the name of registry.
        :param namespace: the name of registry namespace.
        :param repository: the repository name of registry namespace.

        :return: the repository of registry namespace.

        :raise APIError: if server returns an error.
        """
        url = '/registries/{0}/repositories/{1}/{2}'.format(
            registry, namespace, repository
        )

        return self._result(self._get(self._url(url)), json=True)

    def patch_registry_namespaced_repository(self, registry, namespace, repository,
                                             short_description=None, long_description=None,
                                             labels=None):
        """
        Update repository of given registry namespace.

        :param registry: the name of registry.
        :param namespace: the name of registry namespace.
        :param repository: the repository name of registry namespace.
        :param short_description: the short description of repository.
        :param long_description: the long description of repository.
        :param labels: the labels of repository, dict or None.
                       For example:
                            {
                                "io.daocloud.dce.icon": "name=Python"
                            }

        :return: the repository.

        :raise APIError: if server returns an error.
        """
        url = '/registries/{0}/repositories/{1}/{2}'.format(
            registry, namespace, repository
        )

        data = camelize_dict({
            'repo_name': repository,
            'short_description': short_description,
            'long_description': long_description,
            'labels': labels or {}
        })

        return self._result(
            self._patch(self._url(url), json=data), json=True
        )

    def delete_registry_namespaced_repository(self, registry, namespace, repository):
        """
        Delete repository of given registry namespace.

        :param registry: the name of registry.
        :param namespace: the name of registry namespace.
        :param repository: the repository name of registry namespace.

        :raise APIError: if server returns an error.
        """
        url = '/registries/{0}/repositories/{1}/{2}'.format(
            registry, namespace, repository
        )

        res = self._delete(self._url(url))
        self._raise_for_status(res)

    def check_registry_namespaced_repository_tags(self, registry, namespace, repository,
                                                  tags=None):
        """
        Check the repository tags of registry namespace.

        :param registry: the name of registry.
        :param namespace: the name of registry namespace.
        :param repository: the repository name of registry namespace.
        :param tags: a string array of tags.

        :return: a dict only including `RelatedTable` field.

        :raise APIError: if server returns an error.
        """
        url = '/registries/{0}/repositories/{1}/{2}/check-tags'.format(
            registry, namespace, repository
        )

        return self._result(
            self._post(self._url(url), json={'Tags': tags or []}),
            json=True
        )

    def list_registry_namespaced_repository_tags(self, registry, namespace, repository):
        """
        Get repository tags of registry namespace.

        :param registry: the name of registry.
        :param namespace: the name of registry namespace.
        :param repository: the repository name of registry namespace.

        :return: a list of dicts, one per tag.

        :raise APIError: if server returns an error.
        """
        url = '/registries/{0}/repositories/{1}/{2}/tags'.format(
            registry, namespace, repository
        )

        return self._result(self._get(self._url(url)), json=True)

    def copy_registry_namespaced_repository_tag(self, registry, namespace, repository,
                                               src_tag=None, dst_tag=None):
        """
        Copy repository tag of registry namespace.

        :param registry: the name of registry.
        :param namespace: the name of registry namespace.
        :param repository: the repository name of registry namespace.
        :param src_tag: the source tag.
        :param dst_tag: the target tag.

        :raise APIError: if server returns an error.
        """
        url = '/registries/{0}/repositories/{1}/{2}/tags'.format(
            registry, namespace, repository
        )
        data = camelize_dict({
            'src_tag': src_tag,
            'dst_tag': dst_tag
        })

        res = self._post(self._url(url), json=data)
        self._raise_for_status(res)

    def read_registry_info(self, registry):
        """
        Read registry information.

        :param registry: the name of registry.

        :return: the registry.

        :raise APIError: if server returns an error.
        """
        url = '/registries/{0}/info'.format(registry)

        return self._result(self._get(self._url(url)), json=True)

    def search_image_in_registry(self, query_name=None):
        """
        Search registry image by name.

        :param query_name: the name of registry image.

        :return: a list of images, one per image.

        :raise APIError: if server returns an error.
        """
        url = '/registries/search'

        return self._result(
            self._get(self._url(url), params={'QueryName': query_name}),
            json=True
        )

    def search_repository_and_image_in_registry(self, prefix=None):
        """
        Search registry image.

        :param prefix: the prefix of repository or image.

        :return: a dict including `ByRepoName` and `ByName` fields,
                 value of `ByRepoName` field is a list of dict, one per repository,
                 value of `ByName` field is a list of dict, one per image.

        :raise APIError: if server returns an error.
        """
        url = '/registry/auto-complete'

        return self._result(
            self._get(self._url(url), params={'Prefix': prefix}),
            json=True
        )

    def statistic_repository_count_for_every_registry(self):
        """
        Statistic repository count for all registry.

        :return: a dict including `All` and `Registries` fields,
                 value of `All` field is a integer representing repository count,
                 value of `Registries` field is a dict including repository count
                 for every registry.

        :raise APIError: if server returns an error.
        """
        url = '/registries-utils/counts'

        return self._result(self._get(self._url(url)), json=True)


wrap_checking_resource(RegistryApiMixin)
