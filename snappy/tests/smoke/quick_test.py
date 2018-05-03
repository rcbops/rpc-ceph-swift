from snappy.decorators import (DataDrivenFixture, data_driven_test)
from snappy.decorators import DataDrivenFixture
from snappy.generators import ObjectDatasetList


from snappy.fixtures.swift_fixtures import ObjectStorageFixture

@DataDrivenFixture
class QuickTest(ObjectStorageFixture):
    def test_create_container(self):
        response = self.client.create_container('quick_test_container')
        self.assertTrue(response.ok)

        response = self.client.delete_container('quick_test_container')
        self.assertTrue(response.ok)

    @data_driven_test(ObjectDatasetList())
    def ddtest_create_object(self, object_type, generate_object):
        container_name = self.create_temp_container(
            descriptor='quick_test_container')
        object_name = Constants.VALID_OBJECT_NAME
        generate_object(container_name, object_name)

        response = self.client.get_object(container_name, object_name)
        self.assertEqual(200, response.status_code, 'should return object')
