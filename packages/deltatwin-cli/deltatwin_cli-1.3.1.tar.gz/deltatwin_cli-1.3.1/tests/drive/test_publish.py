import json
import os
import unittest
from unittest import mock

from delta.cli.drive.publish import prepare_publish
from tests.utils import RepoMock, FailPushObjMock, GoodPushObjMock


class TestDrivePublish(unittest.TestCase):
    service_url = 'https://delta_api'
    resource_dir = os.path.join(os.path.dirname(__file__), '../resources')
    conf = {}

    @classmethod
    def setUpClass(cls) -> None:
        with open(os.path.join(cls.resource_dir,
                               'drive/manifest_example.json')) as exp:
            with open('manifest.json', 'w') as f:
                json.dump(json.loads(exp.read()), f)
        with open('workflow.yml', 'w'):
            pass

    @classmethod
    def tearDownClass(cls) -> None:
        if os.path.exists("manifest.json"):
            os.remove("manifest.json")
        if os.path.exists("workflow.yml"):
            os.remove("workflow.yml")

    @mock.patch("delta.cli.drive.publish.prepare_publish_to_harbor")
    def test_prepare_publish_version(self, mock_harbor):
        version = ''
        visibility = ''
        topic = ''
        change_log = ''
        manifest = ''
        mock_harbor.return_value = None
        with self.assertRaises(SystemExit) as cm:
            prepare_publish(self.conf, version, visibility,
                            topic, change_log, manifest)

        self.assertEqual(cm.exception.code, 6)

        version = "1.0.0"

        data_version = prepare_publish(
            self.conf,
            version,
            visibility,
            topic,
            change_log,
            manifest)['version']

        self.assertEqual(version, data_version)

        version = "1.0.0.dev2"

        data_version = prepare_publish(
            self.conf,
            version,
            visibility,
            topic,
            change_log,
            manifest,)['version']

        self.assertEqual(version, data_version)
