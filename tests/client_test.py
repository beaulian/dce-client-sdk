# coding=utf-8
import unittest
import six

from dce import (
    APIClient, NullResource
)
from dce.consts import DCE_MODES
from tests.envs import *


class ClientTest(unittest.TestCase):
    api28 = APIClient(DCE_HOST_2_8, username=DCE_USERNAME, password=DCE_PASSWORD)

    def test_ping(self):
        self.assertEqual(self.api28.ping(), 'OK')

    def test_now(self):
        self.assertIsInstance(self.api28.now(), float)

    def test_info(self):
        self.assertIsInstance(self.api28.cluster_uuid, six.string_types)
        self.assertIsInstance(self.api28.virt_tech, six.string_types)
        self.assertIsInstance(self.api28.virt_tech_type, six.string_types)
        self.assertIsInstance(self.api28.stream_room, six.string_types)

        self.assertIn(self.api28.mode, DCE_MODES)
        self.assertIn(self.api28.network_driver, ('calico', 'flannel'))

    def test_check_resource(self):
        with self.assertRaises(NullResource):
            self.api28.reset_account_passord(None)
        self.assertIsInstance(self.api28.list_access_key(), list)
