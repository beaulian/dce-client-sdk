# coding=utf-8
from ..utils import (
    camelize_dict, check_bool_str,
    wrapper_check_resource
)

# 旧式类，可修改__dict__属性
class RegistryApiMixin:
    def list_registry_namespace(self, registry):
        url = '/registries/{0}/namespaces'.format(registry)

        return self._result(self._get(self._url(url)), json=True)

    def create_registry_namespace(self, registry, name=None):
        url = '/registries/{0}/namespaces'.format(registry)

        return self._result(
            self._post(self._url(url), json={'Name': name})
        )

    def read_registry_namespace(self, registry, namespace):
        url = '/registries/{0}/namespaces/{1}'.format(registry, namespace)

        return self._result(self._get(self._url(url)), json=True)

    def patch_registry_namespace(self, registry, namespace,
                                 short_description=None, visibility=None):
        url = '/registries/{0}/namespaces/{1}'.format(registry, namespace)
        data = camelize_dict({
            'short_description': short_description,
            'visibility': visibility
        })

        return self._result(self._post(self._url(url), json=data))

    def delete_registry_namespace(self, registry, namespace):
        url = '/registries/{0}/namespaces/{1}'.format(registry, namespace)

        return self._result(self._delete(self._url(url)))

    def authorize_team_for_registry_namespace(self, registry, namespace,
                                              team_id=None, role=None):
        url = '/registries/{0}/namespaces/{1}/accessible-list'.format(registry, namespace)
        data = camelize_dict({
            'team_id': team_id,
            'role': role
        })

        return self._result(self._post(self._url(url), json=data))

    def unauthorize_team_from_registry_namespace(self, registry, namespace, team_id=None):
        url = '/registries/{0}/namespaces/{1}/accessible-list'.format(registry, namespace)

        return self._result(
            self._delete(self._url(url), params={'TeamId': team_id}),
            json=True
        )

    def list_repository_for_all_registry_namespaces(self, registry, with_remote='True',
                                                    iter=False, limit=None):
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
        url = '/registries/{0}/repositories/{1}'.format(registry, namespace)

        if iter or limit:
            return self._advanced_result(self._advanced_get(self._url(url)),
                                         iter=iter, limit=limit, json=True)
        else:
            return self._result(self._get(self._url(url)), json=True)

    def create_registry_namespaced_repository(self, registry, namespace, repo_name=None,
                                              short_description=None, long_description=None,
                                              labels=None):
        url = '/registries/{0}/repositories/{1}'.format(registry, namespace)

        data = camelize_dict({
            'repo_name': repo_name,
            'short_description': short_description,
            'long_description': long_description,
            'labels': labels or {}
        })

        return self._result(self._post(self._url(url), json=data))

    def read_registry_namespaced_repository(self, registry, namespace, repository):
        url = '/registries/{0}/repositories/{1}/{2}'.format(
            registry, namespace, repository
        )

        return self._result(self._get(self._url(url)), json=True)

    def patch_registry_namespaced_repository(self, registry, namespace, repository,
                                             short_description=None, long_description=None,
                                             labels=None):
        url = '/registries/{0}/repositories/{1}/{2}'.format(
            registry, namespace, repository
        )

        data = camelize_dict({
            'repo_name': repository,
            'short_description': short_description,
            'long_description': long_description,
            'labels': labels or {}
        })

        return self._result(self._patch(self._url(url), json=data))

    def delete_registry_namespaced_repository(self, registry, namespace, repository):
        url = '/registries/{0}/repositories/{1}/{2}'.format(
            registry, namespace, repository
        )

        return self._result(self._delete(self._url(url)))

    def check_registry_namespaced_repository_tags(self, registry, namespace, repository,
                                                  tags=None):
        url = '/registries/{0}/repositories/{1}/{2}/check-tags'.format(
            registry, namespace, repository
        )

        return self._result(
            self._post(self._url(url), json={'Tags': tags or []})
        )

    def list_registry_namespaced_repository_tags(self, registry, namespace, repository):
        url = '/registries/{0}/repositories/{1}/{2}/tags'.format(
            registry, namespace, repository
        )

        return self._result(self._get(self._url(url)), json=True)

    def add_registry_namespaced_repository_tag(self, registry, namespace, repository,
                                               src_tag=None, dst_tag=None):
        url = '/registries/{0}/repositories/{1}/{2}/tags'.format(
            registry, namespace, repository
        )
        data = camelize_dict({
            'src_tag': src_tag,
            'dst_tag': dst_tag
        })

        return self._result(self._post(self._url(url), json=data))

    def read_registry_info(self, registry):
        url = '/registries/{0}/info'.format(registry)

        return self._result(self._get(self._url(url)), json=True)

    def search_registry_image(self, query_name=None):
        url = '/registries/search'

        return self._result(
            self._get(self._url(url), params={'QueryName': query_name}),
            json=True
        )

    def auto_complete_registry_image(self, prefix=None):
        url = '/registry/auto-complete'

        return self._result(
            self._get(self._url(url), params={'Prefix': prefix}),
            json=True
        )

    def read_registry_count(self):
        url = '/registries-utils/counts'

        return self._result(self._get(self._url(url)), json=True)


wrapper_check_resource(RegistryApiMixin)
