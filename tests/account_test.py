# coding=utf-8
import six
import json
import unittest

from dce import APIClient
from tests.envs import *


class AccountTest(unittest.TestCase):
    api28 = APIClient(DCE_HOST_2_8, username=DCE_USERNAME, password=DCE_PASSWORD)

    def test_create_account(self):
        account = self.api28.create_account(name="test", password="test", email="870402916@qq.com")
        self.assertEqual(json.loads(account)['Name'], "test")

    def test_list_account(self):
        accounts = self.api28.list_account()
        self.assertIsInstance(accounts, dict)

    def test_read_my_account(self):
        account = self.api28.read_my_account()
        self.assertEqual(account['Name'], DCE_USERNAME)

    def test_patch_my_account(self):
        account = self.api28.patch_my_account(email="870402916@qq.com")
        self.assertEqual(json.loads(account)['Email'], "870402916@qq.com")

    def test_read_account(self):
        account = self.api28.read_account("test")
        self.assertEqual(account['Name'] == "test")

    def test_patch_account(self):
        account = self.api28.patch_account("test", email="870402916@qq.com")
        self.assertEqual(json.loads(account)['Email'], "870402916@qq.com")

    def test_delete_account(self):
        self.api28.delete_account("test")
        account = self.api28.read_account("test")
        self.assertTrue("error_id" in account)




