# coding=utf-8
from ..utils import (
    camelize_dict, check_bool_str,
    wrap_checking_resource
)


class AccessKeyApiMixin:
    def list_access_key(self, iter=False, limit=None):
        """
        Get access keys.

        :param iter: if `True`, return a generator of access keys.
        :param limit: the number of access keys allowed to return
                      if None, return all access keys.

        :return: a list or generator of dicts, one per access key.

        :raise TypeError: if limit is not an integer or None.
        :raise APIError: if server returns an error.
        """
        url = '/access-keys'

        if iter or limit:
            return self._advanced_result(self._advanced_get(self._url(url)),
                                         iter=iter, limit=limit, json=True)
        else:
            return self._result(self._get(self._url(url)), json=True)

    def create_access_key_pair(self):
        """
        Create a access key pair.

        :return: the access key pair.

        :raise APIError: if server returns an error.
        """
        url = '/access-keys'

        return self._result(self._post(self._url(url)), json=True)

    def delete_access_key_pair(self, access_key):
        """
        Delete access key pair.

        :param access_key: the access key to be deleted.

        :raise APIError: if server returns an error.
        """
        url = '/access-keys/{0}'.format(access_key)

        res = self._delete(self._url(url))
        self._raise_for_status(res)


class TeamAPiMixin:
    def list_team(self, all='False', iter=False, limit=None):
        """
        Get teams.

        :param all: if `False`, only return teams of current user,
                    else return all teams.
        :param iter: if `True`, return a generator of teams.
        :param limit: the number of teams allowed to return
                      if None, return all teams.

        :return: a list of dicts, one per team.

        :raise TypeError: if `limit` is neither a integer nor None.
        :raise ValueError: if `all` is not a neither a boolean string nor None.
        :raise APIError: if server returns an error.
        """
        check_bool_str(all=all)

        url = '/teams'
        params = {
            'All': all
        }

        if iter or limit:
            return self._advanced_result(
                self._advanced_get(self._url(url), params=params),
                iter=iter, limit=limit, json=True
            )
        else:
            return self._result(
                self._get(self._url(url), params=params),
                json=True
            )

    def create_team(self, name=None):
        """
        Create team

        :param name: the name of team.

        :return: the team.

        :raise APIError: if server returns an error.
        """
        url = '/teams'

        return self._result(
            self._post(self._url(url), json={'Name': name}),
            json=True
        )

    def read_team(self, team):
        """
        Read the detail of given team

        :param team: the id of team.

        :return: the team.

        :raise APIError: if server returns an error.
        """
        url = '/teams/{0}'.format(team)

        return self._result(self._get(self._url(url)), json=True)

    def patch_team(self, team, name=None):
        """
        Update the name of given team.

        :param team: the id of team.
        :param name: new name of given team.

        :return: the team.

        :raise APIError: if server returns an error.
        """
        url = '/teams/{0}'.format(team)

        return self._result(
            self._patch(self._url(url), json={'Name': name}),
            json=True
        )

    def delete_team(self, team):
        """
        Delete team.

        :param team: the id of team.

        :raise APIError: if server returns an error.
        """
        url = '/teams/{0}'.format(team)

        res = self._delete(self._url(url))
        self._raise_for_status(res)

    def add_team_member(self, team, name=None):
        """
        Add member to team.

        :param team: the id of team.
        :param name: the name of member.

        :return: the team.

        :raise APIError: if server returns an error.
        """
        url = '/teams/{0}/members'.format(team)

        return self._result(
            self._post(self._url(url), json={'Name': name}),
            json=True
        )

    def delete_team_member(self, team, name=None):
        """
        Delete member from team.

        :param team: the id of team.
        :param name: the name of member.

        :raise APIError: if server returns an error.
        """
        url = '/teams/{0}/members'.format(team)

        res = self._delete(self._url(url), params={'Name': name})
        self._raise_for_status(res)


class TenantApiMixin:
    def list_tenant(self, iter=False, limit=None):
        """
        Get tenants.

        :param iter: if `True`, return a generator of tenants.
        :param limit: the number of tenants allowed to return
                      if None, return all tenants.

        :return: a list of dicts, one per tenant.

        :raise TypeError: if limit is not an integer or None.
        :raise APIError: if server returns an error.
        """
        url = '/tenants'

        if iter or limit:
            return self._advanced_result(self._advanced_get(self._url(url)),
                                         iter=iter, limit=limit, json=True)
        else:
            return self._result(self._get(self._url(url)), json=True)

    def list_stat_for_all_tenants(self, iter=False, limit=None):
        """
        Get stats for all tenants.

        :param iter: if `True`, return a generator of stats.
        :param limit: the number of stats allowed to return
                      if None, return all stats.

        :return: a list of dicts, one per stat.

        :raise TypeError: if limit is not an integer or None.
        :raise APIError: if server returns an error.
        """
        url = '/tenants-utils/stats'

        if iter or limit:
            return self._advanced_result(self._advanced_get(self._url(url)),
                                         iter=iter, limit=limit, json=True)
        else:
            return self._result(self._get(self._url(url)), json=True)

    def list_tenant_stat(self, tenant):
        """
        Get stats of given tenant.

        :param tenant: the name of tenant.

        :return: a list of dicts, one per tenant's stat.

        :raise APIError: if server returns an error.
        """
        url = '/tenants/{0}/stats'.format(tenant)

        return self._result(self._get(self._url(url)), json=True)

    def create_tenant(self, name=None):
        """
        Create tenant.

        :param name: the name of tenant.

        :return: the tenant.

        :raise APIError: if server returns an error.
        """
        url = '/tenants'

        return self._result(
            self._post(self._url(url), json={'Name': name}),
            json=True
        )

    def read_tenant(self, tenant):
        """
        Read the detail of given tenant.

        :param tenant: the name of tenant.

        :return: the tenant.

        :raise APIError: if server returns an error.
        """
        url = '/tenants/{0}'.format(tenant)

        return self._result(self._get(self._url(url)), json=True)

    def delete_tenant(self, tenant):
        """
        Delete tenant.

        :param tenant: the name of tenant.

        :raise APIError: if server returns an error.
        """
        url = '/tenants/{0}'.format(tenant)

        res = self._delete(self._url(url))
        self._raise_for_status(res)

    def authorize_team_for_tenant(self, tenant, team_id=None, role=None):
        """
        Authorize team for tenant.

        :param tenant: the name of tenant.
        :param team_id: the id of team.
        :param role: the authorized role: `no_access` or `view_only`
                     or `restricted_control` or `full_control` or `admin`.

        :return: the tenant.

        :raise APIError: if server returns an error.
        """
        url = '/tenants/{0}/accessible-list'.format(tenant)
        data = camelize_dict({
            'team_id': team_id,
            'role': role
        })

        return self._result(
            self._post(self._url(url), json=data), json=True
        )

    def unauthorize_team_from_tenant(self, tenant, team_id=None):
        """
        Cancel team's authorization from tenant.

        :param tenant: the name of tenant.
        :param team_id: the id of team.

        :raise APIError: if server returns an error.
        """
        url = '/tenants/{0}/accessible-list'.format(tenant)

        res = self._delete(self._url(url), params={'TeamId': team_id})
        self._raise_for_status(res)

    def put_tenant_quota(self, tenant, limit_cpu=None, limit_memory=None):
        """
        Update tenant's quota.

        :param tenant: the name of tenant.
        :param limit_cpu: the cpu limit, integer or float.
        :param limit_memory: the memory limit, integer.

        :return: the tenant.

        :raise APIError: if server returns an error.
        """
        url = '/tenants/{0}/quota'.format(tenant)
        data = {
            'LimitCPU': limit_cpu,
            'LimitMemory': limit_memory
        }

        return self._result(self._put(self._url(url), json=data))

    def put_tenant_constraints(self, tenant, constraints=None):
        """
        Update tenant's constraints.

        :param tenant: the name of tenant
        :param constraints: the constraints which restrict the hosts
                            that current tenant can schedule.
                            For example:
                                [
                                    "node.labels.beta.kubernetes.io/arch==amd64"
                                ]

        :return: the tenant.

        :raise APIError: if server returns an error.
        """
        url = '/tenants/{0}/constraints'.format(tenant)

        return self._result(
            self._put(self._url(url), json={'Constraints': constraints or []}),
            json=True
        )


class AccountApiMixin(AccessKeyApiMixin,
                      TeamAPiMixin,
                      TenantApiMixin):
    def list_account(self, search_term=None,
                     sort_by=None, sort_order='asc',
                     iter=False, limit=None):
        """
        Get accounts.

        :param search_term: the searching keywords.
        :param sort_by: the searching area, `name` or `email` or `is_ldap`.
        :param sort_order: the sorting way, `asc` or `desc`.
        :param iter: if `True`, return a generator of accounts.
        :param limit: the number of accounts allowed to return
                      if None, return all accounts.

        :return: a list of dicts, one per account.

        :raise TypeError: if limit is not an integer or None.
        :raise APIError: if server returns an error.
        """
        url = '/accounts'
        params = camelize_dict({
            'search_term': search_term,
            'sort_by': sort_by,
            'sort_order': sort_order
        })

        if iter or limit:
            return self._advanced_result(
                self._advanced_get(self._url(url), params=params),
                iter=iter, limit=limit, json=True
            )
        else:
            return self._result(
                self._get(self._url(url), params=params),
                json=True
            )

    def create_account(self, name=None, email=None,
                       password=None, is_admin='False'):
        """
        Create account.

        :param name: the name of account.
        :param email: the email of account.
        :param password: the password of account.
        :param is_admin: is the account an administrator.

        :return: the account.

        :raise ValueError: if `is_admin` is neither a boolean string nor None.
        :raise APIError: if server returns an error.
        """
        check_bool_str(is_admin=is_admin)

        url = '/accounts'
        data = camelize_dict({
            'name': name,
            'email': email,
            'password': password,
            'is_admin': is_admin
        })

        return self._result(
            self._post(self._url(url), json=data), json=True
        )

    def read_my_account(self):
        """
        Read the detail of current account.

        :return: the account.

        :raise APIError: if server returns an error.
        """
        url = '/my-account'

        return self._result(self._get(self._url(url)), json=True)

    def patch_my_account(self, email=None, password=None):
        """
        Update current account.

        :param email: the email of account.
        :param password: the password of account.

        :return: the account.

        :raise APIError: if server returns an error.
        """
        url = '/my-account'
        data = camelize_dict({
            'email': email,
            'password': password
        })

        return self._result(
            self._patch(self._url(url), json=data), json=True
        )

    def change_my_account_password(self, name=None, old_password=None,
                                   new_password=None):
        """
        Change the password of current account.

        :param name: the name of account.
        :param old_password: the old password of account.
        :param new_password: the new password of account.

        :return: the account.

        :raise APIError: if server returns an error.
        """
        url = '/my-account/change-password'
        data = camelize_dict({
            'name': name,
            'old_password': old_password,
            'new_password': new_password
        })

        return self._result(
            self._post(self._url(url), json=data), json=True
        )

    def read_account(self, account):
        """
        Read the detail of given account.

        :param account: the name of account.

        :return: the account.

        :raise APIError: if server returns an error.
        """
        url = '/accounts/{0}'.format(account)

        return self._result(self._get(self._url(url)), json=True)

    def patch_account(self, account, email=None,
                      password=None, is_admin='False'):
        """
        Update given account.

        :param account: the name of account.
        :param email: the email of account.
        :param password: the password of account.
        :param is_admin: is the account an administrator.

        :return: the account.

        :raise ValueError: if `is_admin` is neither a boolean string nor None.
        :raise APIError: if server returns an error.
        """
        url = '/accounts/{0}'.format(account)
        data = camelize_dict({
            'email': email,
            'password': password,
            'is_admin': is_admin
        })

        return self._result(
            self._patch(self._url(url), json=data), json=True
        )

    def delete_account(self, account):
        """
        Delete account.

        :param account: the name of account.

        :raise APIError: if server returns an error.
        """
        url = '/accounts/{0}'.format(account)

        res = self._delete(self._url(url))
        self._raise_for_status(res)

    def list_account_tenant(self, account, iter=False, limit=None):
        """
        Get account's tenants.

        :param account: the name of account.
        :param iter: if `True`, return a generator of tenants.
        :param limit: the number of tenants allowed to return
                      if None, return all tenants.

        :raise APIError: if server returns an error.
        """
        url = '/accounts/{0}/tenants'.format(account)

        if iter or limit:
            return self._advanced_result(self._advanced_get(self._url(url)),
                                         iter=iter, limit=limit, json=True)
        else:
            return self._result(self._get(self._url(url)), json=True)

    def list_account_team(self, account, iter=False, limit=None):
        """
        Get account's teams.

        :param account: the name of account.
        :param iter: if `True`, return a generator of teams.
        :param limit: the number of teams allowed to return
                      if None, return all teams.

        :raise APIError: if server returns an error.
        """
        url = '/accounts/{0}/teams'.format(account)

        if iter or limit:
            return self._advanced_result(self._advanced_get(self._url(url)),
                                         iter=iter, limit=limit, json=True)
        else:
            return self._result(self._get(self._url(url)), json=True)

    def change_account_password(self, account, password=None):
        """
        Change the password of given account.

        :param account: the name of account.
        :param password: the new password of account.

        :return: the account.

        :raise APIError: if server returns an error.
        """
        url = '/accounts/{0}/change-password'.format(account)

        return self._result(
            self._post(self._url(url), json={'Password': password}),
            json=True
        )

    def authorize_admin(self):
        """
        Authorize administrator.
        The current user must be administrator.

        :return: a empty string.

        :raise APIError: if server returns an error.
        """
        url = '/accounts-utils/auth-admin'

        return self._result(self._get(self._url(url)))


wrap_checking_resource(AccountApiMixin)
