import json

from snappy.constants import Constants
from snappy.fixtures.swift_fixtures import ObjectStorageFixture

CONTENT_TYPE_TEXT = "text/plain; charset=UTF-8"
CONTAINER_NAME = "delimiter_test"


class PrefixTest(ObjectStorageFixture):
    @classmethod
    def setUpClass(cls):
        super(PrefixTest, cls).setUpClass()

        cls.container_name = CONTAINER_NAME
        cls.client.create_container(cls.container_name)

        cls.object_data = Constants.VALID_OBJECT_DATA
        cls.content_length = str(len(cls.object_data))
        cls.headers = {'Content-Length': cls.content_length,
                       'Content-Type': CONTENT_TYPE_TEXT}

    @classmethod
    def tearDownClass(cls):
        super(PrefixTest, cls).setUpClass()
        cls.behaviors.force_delete_containers([cls.container_name])

    def test_prefix(self):
        prefix = "music"

        self.client.create_object(
            self.container_name,
            "music_play_list",
            headers=self.headers,
            data=self.object_data)

        self.client.create_object(
            self.container_name,
            "must_have_slurm",
            headers=self.headers,
            data=self.object_data)

        self.client.create_object(
            self.container_name,
            "music/grok",
            headers=self.headers,
            data=self.object_data)

        self.client.create_object(
            self.container_name,
            "music/drok",
            headers=self.headers,
            data=self.object_data)

        self.client.create_object(
            self.container_name,
            "music/the_best_of_grok_and_drok/",
            headers=self.headers,
            data=self.object_data)

        params = {"prefix": prefix, "format": "json"}
        response = self.client.list_objects(self.container_name, params=params)

        content = None

        try:
            content = json.loads(response.content)
        except ValueError, error:
            self.fixture_log.exception(error)

        members = []
        for member in content:
            if "subdir" in member.keys():
                members.append(member["subdir"])
            elif "name" in member.keys():
                members.append(member["name"])
            else:
                continue

        self.assertTrue(response.ok)

        expected = 4
        received = len(members)

        self.assertEqual(
            expected,
            received,
            msg="expected {0} members in the response, received {1}".format(
                expected,
                received))
        self.assertIn(
            "music_play_list",
            members,
            msg="music_play_list was not in the response")
        self.assertIn(
            "music/grok",
            members,
            msg="music/grok was not in the response")
        self.assertIn(
            "music/drok",
            members,
            msg="music/drok was not in the response")
        self.assertIn(
            "music/the_best_of_grok_and_drok/",
            members,
            msg="music/the_best_of_grok_and_drok/ was not in the response")
