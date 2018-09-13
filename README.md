# snappy

smoke, regression and feature tests for object storage.

initial ground work to decafinize the existing object
storage repo and port from unit test to pytest.

# tests are run using pytest's runner:
pytest --config=/path/to/configs/test.config -v --capture=no tests/

# example config:

```[user_auth_config]
endpoint = https://staging.identity.api.rackspacecloud.com
strategy = rax_auth

[user]
username = <USER_NAME_STUB>
api_key = <API_KEY_STUB>

[objectstorage]
identity_service_name = cloudFiles
region = PPROD

[objectstorage_api]
features = __ALL__
default_content_length = 0
base_container_name = qe_cf
base_object_name = qe_cf_object
http_headers_per_request_count = 90
http_headers_combined_max_len = 4096
http_request_line_max_len = 8192
http_request_max_content_len = 5368709120
containers_name_max_len = 256
containers_list_default_count = 1000
containers_list_default_max_count = 1000
containers_max_count = 500000
object_name_max_len = 1024
object_max_size = 5368709120
object_metadata_max_count = 90
object_metadata_combined_byte_len = 4096
object_list_default_count = 1000
object_list_default_max_count = 1000
metadata_name_max_len = 128
metadata_value_max_len = 256
tempurl_key_cache_time = 60
formpost_key_cache_time = 60
bulk_delete_max_count = 10000
min_slo_segment_size = 1024
max_slo_segment_count = 1000
auth_cache_listener_timeout = 600
strict_cors_mode = False
object_deletion_wait_interval = 90
max_retry_count = 5
retry_sleep_time = 5

[cdn]
region = PPROD
identity_service_name = cloudFilesCDN

[cdn_api]
max_ttl = 1576800000
min_ttl = 900
default_ttl = 259200```

