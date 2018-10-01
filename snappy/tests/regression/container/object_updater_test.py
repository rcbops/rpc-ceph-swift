from snappy.swift_fixtures import ObjectStorageFixture

CONTENT_TYPE_TEXT = 'text/plain; charset=UTF-8'
CONTAINER_NAME = 'container_obj_count_test'


class ObjectUpdaterTest(ObjectStorageFixture):
    @classmethod
    def setUpClass(cls):
        super(ObjectUpdaterTest, cls).setUpClass()

        cls.obj_names = ["a_obj", "b_obj", "c_obj", "d_obj", "e_obj", "f_obj"]

    def test_x_container_object_count_head_get_equivelent(self):
        get_count = 0
        head_count = 0

        container_name = self.behaviors.generate_unique_container_name(
            CONTAINER_NAME)

        self.behaviors.create_container(container_name)

        object_data = 'Test file data'
        content_length = str(len(object_data))
        headers = {'Content-Length': content_length,
                   'Content-Type': CONTENT_TYPE_TEXT}

        for obj_name in self.obj_names:
            self.behaviors.create_object(
                container_name,
                obj_name,
                headers=headers,
                data=object_data)

        self.addCleanup(
            self.behaviors.force_delete_containers,
            [container_name])

        get_response = self.client.list_objects(container_name)
        head_response = self.client.get_container_metadata(container_name)

        get_count = int(get_response.headers.get('x-container-object-count'))
        head_count = int(head_response.headers.get('x-container-object-count'))

        self.assertEqual(
            get_count,
            head_count,
            msg="GET x-container-object-count: {0} HEAD"
            " x-container-object-count: {1}".format(get_count, head_count))

    def test_x_container_object_count_with_update(self):
        updated_get_count = 0
        updated_head_count = 0
        num_created_containers = 0

        container_name = self.behaviors.generate_unique_container_name(
            CONTAINER_NAME)

        self.behaviors.create_container(container_name)

        object_data = 'Test file data'
        content_length = str(len(object_data))
        headers = {'Content-Length': content_length,
                   'Content-Type': CONTENT_TYPE_TEXT}

        for obj_name in self.obj_names:
            response = self.client.create_object(
                container_name,
                obj_name,
                headers=headers,
                data=object_data)

            if response.ok:
                num_created_containers += 1

        self.addCleanup(
            self.behaviors.force_delete_containers,
            [container_name])

        get_response = self.client.list_objects(container_name)

        head_response = self.client.get_container_metadata(container_name)

        updated_get_count = int(get_response.headers.get(
            'x-container-object-count'))

        updated_head_count = int(head_response.headers.get(
            'x-container-object-count'))

        self.assertEqual(
            num_created_containers,
            updated_get_count,
            msg="GET x-container-object-count expected: {0}"
            " x-container-object-count received: {1}".format(
                num_created_containers,
                updated_get_count))

        self.assertEqual(
            updated_head_count,
            num_created_containers,
            msg="HEAD x-container-object-count expected: {0}"
            " x-container-object-count received: {1}".format(
                num_created_containers,
                updated_head_count))

        self.client.delete_object(container_name, self.obj_names[0])

        get_response = self.client.list_objects(container_name)

        head_response = self.client.get_container_metadata(container_name)

        expected_get_count = num_created_containers - 1

        expected_head_count = num_created_containers - 1

        updated_get_count = int(get_response.headers.get(
            'x-container-object-count'))

        updated_head_count = int(head_response.headers.get(
            'x-container-object-count'))

        self.assertEqual(
            expected_get_count,
            updated_get_count,
            msg="GET x-container-object-count expected: {0}"
            " x-container-object-count received: {1}".format(
                expected_get_count,
                updated_get_count))

        self.assertEqual(
            expected_head_count,
            updated_head_count,
            msg="HEAD x-container-object-count expected: {0}"
            " x-container-object-count received: {1}".format(
                expected_head_count,
                updated_head_count))
