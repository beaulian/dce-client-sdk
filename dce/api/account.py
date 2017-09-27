# coding=utf-8
from ..utils import (
    camelize_dict, check_bool_str,
    wrapper_check_resource
)


class AccessKeyApiMixin:
    def list_access_key(self):
        url = '/access-keys'

        return self._result(self._get(self._url(url)), json=True)

    def create_access_key_pair(self):
        url = '/access-keys'

        return self._result(self._post(self._url(url)))

    def delete_access_key_pair(self, access_key):
        url = '/access-keys/{0}'.format(access_key)

        return self._result(self._delete(self._url(url)))


class TeamAPiMixin:
    def list_team(self, all='False'):
        check_bool_str(all=all)

        url = '/teams'

        return self._result(
            self._get(self._url(url), params={'All': all}),
            json=True
        )

    def create_team(self, name=None):
        url = '/teams'

        return self._result(
            self._post(self._url(url), json={'Name': name})
        )

    def read_team(self, team):
        url = '/teams/{0}'.format(team)

        return self._result(self._get(self._url(url)), json=True)

    def patch_team(self, team, name=None):
        url = '/teams/{0}'.format(team)

        return self._result(
            self._patch(self._url(url), json={'Name': name})
        )

    def delete_team(self, team):
        url = '/teams/{0}'.format(team)

        return self._result(self._delete(self._url(url)))

    def add_team_member(self, team, name=None):
        url = '/teams/{0}/members'.format(team)

        return self._result(
            self._post(self._url(url), json={'Name': name})
        )

    def delete_team_member(self, team, name=None):
        url = '/teams/{0}/members'.format(team)

        return self._result(
            self._delete(self._url(url), params={'Name': name})
        )


class TenantApiMixin:
    def list_tenant(self):
        url = '/tenants'

        return self._result(self._get(self._url(url)), json=True)

    def list_stat_for_all_tenants(self):
        url = '/tenants-utils/stats'

        return self._result(self._get(self._url(url)), json=True)

    def list_tenant_stat(self, tenant):
        url = '/tenants/{0}/stats'.format(tenant)

        return self._result(self._get(self._url(url)), json=True)

    def create_tenant(self, name=None):
        url = '/tenants'

        return self._result(
            self._post(self._url(url), json={'Name': name})
        )

    def read_tenant(self, tenant):
        url = '/tenants/{0}'.format(tenant)

        return self._result(self._get(self._url(url)), json=True)

    def delete_tenant(self, tenant):
        url = '/tenants/{0}'.format(tenant)

        return self._result(self._delete(self._url(url)))

    def authorize_team_for_tenant(self, tenant, team_id=None, role=None):
        url = '/tenants/{0}/accessible-list'.format(tenant)
        data = camelize_dict({
            'team_id': team_id,
            'role': role
        })

        return self._result(self._post(self._url(url), json=data))

    def unauthorize_team_from_tenant(self, tenant, team_id=None):
        url = '/tenants/{0}/accessible-list'.format(tenant)

        return self._result(
            self._delete(self._url(url), params={'TeamId': team_id}),
            json=True
        )

    def put_tenant_quota(self, tenant, limit_cpu=None, limit_memory=None):
        url = '/tenants/{0}/quota'.format(tenant)
        data = {
            'LimitCPU': limit_cpu,
            'LimitMemory': limit_memory
        }

        return self._result(self._put(self._url(url), json=data))

    def put_tenant_constraints(self, tenant, constraints=None):
        url = '/tenants/{0}/constraints'.format(tenant)

        return self._result(
            self._put(self._url(url), json={'Constraints': constraints or []})
        )


class AccountApiMixin(AccessKeyApiMixin,
                      TeamAPiMixin,
                      TenantApiMixin):
    def list_account(self, search_team=None, sort_by=None, sort_order='asc'):
        url = '/accounts'
        params = camelize_dict({
            'search_team': search_team,
            'sort_by': sort_by,
            'sort_order': sort_order
        })

        return self._result(
            self._get(self._url(url), params=params),
            json=True
        )

    def create_account(self, name=None, email=None, password=None, is_admin='False'):
        check_bool_str(is_admin=is_admin)

        url = '/accounts'
        data = camelize_dict({
            'name': name,
            'email': email,
            'password': password,
            'is_admin': is_admin
        })

        return self._result(self._post(self._url(url)))

    def read_my_account(self):
        url = '/my-account'

        return self._result(self._get(self._url(url)), json=True)

    def patch_my_account(self, email=None, password=None):
        url = '/my-account'
        data = camelize_dict({
            'email': email,
            'password': password
        })

        return self._result(self._patch(self._url(url), json=data))

    def change_my_account_password(self, name=None, old_password=None,
                                   new_password=None):
        url = '/my-account/change-password'
        data = camelize_dict({
            'name': name,
            'old_password': old_password,
            'new_password': new_password
        })

        return self._result(self._post(self._url(url), json=data))

    def read_account(self, account):
        url = '/accounts/{0}'.format(account)

        return self._result(self._get(self._url(url)), json=True)

    def patch_account(self, account, email=None, password=None, is_admin='False'):
        url = '/accounts/{0}'.format(account)
        data = camelize_dict({
            'email': email,
            'password': password,
            'is_admin': is_admin
        })

        return self._result(self._patch(self._url(url), json=data))

    def delete_account(self, account):
        url = '/accounts/{0}'.format(account)

        return self._result(self._delete(self._url(url)), json=True)

    def list_account_tenant(self, account):
        url = '/accounts/{0}/tenants'.format(account)

        return self._result(self._get(self._url(url)), json=True)

    def list_account_team(self, account):
        url = '/accounts/{0}/teams'.format(account)

        return self._result(self._get(self._url(url)), json=True)

    def change_account_password(self, account, password=None):
        url = '/accounts/{0}/change-password'.format(account)

        return self._result(
            self._post(self._url(url), json={'Password': password})
        )

    def reset_account_passord(self, account):
        url = '/accounts/reset-password'

        return self._result(
            self._post(self._url(url), json={'Name': account})
        )

    def read_account_reseted_password(self, key=None):
        url = '/accounts/reset-password'

        return self._result(
            self._get(self._url(url), params={'Key': key}),
            json=True
        )

    def authorize_admin(self):
        url = '/accounts-utils/auth-admin'

        return self._result(self._get(self._url(url)))


wrapper_check_resource(AccountApiMixin)
