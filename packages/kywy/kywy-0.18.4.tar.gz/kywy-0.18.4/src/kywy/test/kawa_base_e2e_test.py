import os
import unittest
from ..client.kawa_client import KawaClient as kawa
from dotenv import load_dotenv

load_dotenv()

kawa_url = os.environ['E2E_KAWA_URL']
kawa_api_key_user_1 = os.environ['E2E_KAWA_API_KEY_USER_1']
kawa_api_key_user_2 = os.environ['E2E_KAWA_API_KEY_USER_2']
workspace = os.getenv('E2E_KAWA_WORKSPACE', 1)


class KawaBaseTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('Setup tests in workspace {} on url {}'.format(workspace, kawa_url))
        k = kawa(kawa_api_url=kawa_url)
        k_second_user = kawa(kawa_api_url=kawa_url)

        k.set_api_key(api_key=kawa_api_key_user_1)
        k.set_active_workspace_id(workspace_id=workspace)
        cls.kawa = k
        cls.commands = k.commands
        cls.workspace_id = workspace

        k_second_user.set_api_key(api_key=kawa_api_key_user_2)
        k_second_user.set_active_workspace_id(workspace_id=workspace)
        cls.kawa_second_user = k_second_user
        cls.commands_second_user = k_second_user.commands
