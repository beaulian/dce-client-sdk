# coding=utf-8
import unittest
import six

from dce import APIClient
from tests.envs import *


class AccountTest(unittest.TestCase):
    api28 = APIClient(DCE_HOST_2_8, username=DCE_USERNAME, password=DCE_PASSWORD)

    # to do.
