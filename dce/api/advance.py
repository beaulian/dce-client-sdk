# coding=utf-8
import json as to_json


def json_loads(text, **kwargs):
    from requests.utils import guess_json_utf

    encoding = guess_json_utf(text)
    if encoding is not None:
        try:
            return to_json.loads(text.decode(encoding).strip(',\n\t '), **kwargs)
        except UnicodeDecodeError:
            pass

    return to_json.loads(text, **kwargs)


class IterResult(object):
    def _advanced_get(self, url, **kwargs):
        kwargs.setdefault('stream', True)

        return self._request('GET', url, **kwargs)

    @staticmethod
    def __get_result(response, limit=None, json=False):

        if limit is not None and not isinstance(limit, int):
            raise TypeError(
                "'limit' got an unexpected type: {0}, expected int or None".format(
                    limit
                )
            )

        def iter_object():
            record = 0
            start = False
            container = []
            for line in response.iter_lines():
                if '{' in line:
                    start = True
                    record += 1
                elif '}' in line:
                    record -= 1
                if start:
                    container.append(line)
                    if record == 0:
                        if json:
                            yield json_loads(''.join(container))
                        else:
                            yield ''.join(container)
                        start = False
                        container = []
        if limit:
            count = 1
            for object_ in iter_object():
                if limit >= count:
                    yield object_
                    count += 1
        else:
            for object_ in iter_object():
                yield object_
        # release connection
        response.close()

    def _advanced_result(self, response, iter=True, limit=None, json=False):
        self._raise_for_status(response)
        result = self.__get_result(response, limit=limit, json=json)

        return result if iter else list(result)


class CreateAccountWithTTRN(object):
    def create_account_with_ttrn(self, name=None, email=None,
                                 password=None, is_admin='False',
                                 registry='buildin-registry',
                                 limit_cpu=0, limit_memory=0):
        self.create_account(
            name=name,
            email=email,
            password=password,
            is_admin=is_admin
        )
        team = to_json.loads(self.create_team(name))
        tenant = to_json.loads(self.create_tenant(name))
        registry_namespace = to_json.loads(
            self.create_registry_namespace(registry, name=name)
        )

        if team:
            team['Members'].append(name)
            self.add_team_member(team['Id'], name=name)
        if tenant and not (limit_cpu or limit_memory):
            self.put_tenant_quota(tenant['Name'], limit_cpu=limit_cpu,
                                  limit_memory=limit_memory)
        if registry_namespace and team:
            self.authorize_team_for_registry_namespace(registry, registry_namespace['Name'],
                                                       team_id=team['Id'], role='full_control')
            self.patch_registry_namespace(registry, registry_namespace['Name'],
                                          visibility='False')


class AdvancedMethodMixin(IterResult,
                          CreateAccountWithTTRN):
    pass
