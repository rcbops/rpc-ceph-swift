from snappy.common.data_interfaces import ConfigSectionInterface


class ObjectStorageConfig(ConfigSectionInterface):
    """
    Product config for retrieving info from the service catalog.
    """

    SECTION_NAME = 'objectstorage'

    @property
    def identity_service_name(self):
        """
        Service name to use.
        """
        return self.get('identity_service_name')

    @property
    def region(self):
        """
        Region to use.
        """
        return self.get('region')


class ObjectStorageAPIConfig(ConfigSectionInterface):
    """
    API Settings for ObjectStorage.
    """

    SECTION_NAME = 'objectstorage_api'

    ALL_FEATURES = '__ALL__'
    NO_FEATURES = '__NONE__'

    @property
    def base_container_name(self):
        """
        String to be prepended to created container names.
        In general most containers will be created using this convention,
        but there may be some test cases which warrant ignoring this value.
        """
        return self.get('base_container_name', '')

    @property
    def object_expirer_run_interval(self):
        """
        Interval in seconds that the object expirer is expected to run
        and complete.
        """
        return int(self.get('object_expirer_run_interval', '60'))

    @property
    def use_swift_info(self):
        """
        If True, tells CloudCafe to make a call to swift's /info resource
        to determine the features available.  If false, all features must
        be provided via the config.
        """
        return self.get_boolean('use_swift_info', True)

    @property
    def version(self):
        """
        Specify the version of swift running allowing tests tagged with the
        required_version decorator to skip tests based on version rules.
        This version is to be used if provided, even if a different version
        is returned from a /info call.
        """
        return self.get('version', '')

    @property
    def features(self):
        """
        Tests can be tagged with a decorator as follows:
        @ObjectStorageFixture.required_features('feature1', 'feature2')
        These tagged tests, will only be run if all of the features listed have
        been added to the features key.  If use_swift_info is true, features
        will be pulled from the swift info and added to the features defined
        here.
        The features are defined by adding them to a whitespace separated list
        as follows:
            features=foo bar ...
        The following special values can also be set:
            __ALL__  - runs all tests tagged with required_features,
                       regardless of the features listed in the decorator.
            __NONE__ - runs no tests tagged with required_features, regardless
                       of the features listed in the decorator.
        by defaut, no features are added.
        """
        return self.get('features', '')

    @property
    def excluded_features(self):
        """
        In addition to setting the features, you can also exclude features from
        being reported.  If for example you have the following:
            features=foo bar
            excluded_features=foo
        This will have the same efect as the following:
            features=bar

        By default, no excluded features are set.
        """
        return self.get('excluded_features', '')

    @property
    def max_container_name_len(self):
        """
        Max container name length in bytes.
        """
        return int(self.get('max_container_name_len', 256))

    @property
    def containers_listing_default_count(self):
        """
        Default object count returned for a container listing.
        """
        return int(self.get('containers_list_default_count',
                            self.container_listin_limit))

    @property
    def container_listing_limit(self):
        """
        Max object count for a container listing.
        """
        return int(self.get('container_listing_limit', 10000))

    @property
    def max_object_name_len(self):
        """
        Maximum length in bytes for a object name.
        """
        return int(self.get('max_object_name_len', 1024))

    @property
    def max_object_size(self):
        """
        Maximum object size in bytes.
        """
        return int(self.get('max_object_size', 5368709122))

    @property
    def object_metadata_max_count(self):
        """
        Maximum number of distinct metadata items.
        """
        return int(self.get('object_metadata_max_count', 90))

    @property
    def max_metadata_overall_size(self):
        """
        Maximum number of bytes allowed for combined container/object
        metadata.
        """
        return int(self.get('max_metadata_overall_size', 4096))

    @property
    def account_listing_limit(self):
        """
        Max container list length of a account listing.
        """
        return self.get('object_list_default_count')

    @property
    def metadata_name_max_len(self):
        """
        Maximum length in bytes allowed for metadata names.
        This does not include the bytes needed for the 'X-Container-Meta-' and
        'X-Object-Meta-' portion of header used to set metadata.
        """
        return int(self.get('metadata_name_max_len', 128))

    @property
    def metadata_value_max_len(self):
        """
        Maximum length in bytes allowed for metadata values.
        """
        return int(self.get('metadata_value_max_len', 256))

    @property
    def tempurl_key_cache_time(self):
        """
        The amount of time that keys for tempurl are cached.
        """
        return int(self.get('tempurl_key_cache_time', 0))

    @property
    def formpost_key_cache_time(self):
        """
        The amount of time that keys for formpost are cached.
        """
        return int(self.get('formpost_key_cache_time', 0))

    @property
    def min_slo_segment_size(self):
        """
        The smallest size in bytes of a non-terminal static large object
        segment.
        """
        return int(self.get('min_slo_segment_size', 1048576))

    @property
    def list_timeout(self):
        """
        The timeout in seconds to stop retrying container/object listings
        and instead report an error.
        """
        return int(self.get('list_timeout', 120))

    @property
    def info_admin_key(self):
        """
        The admin key for admin /info calls.
        """
        return self.get('info_admin_key', '')

    @property
    def strict_cors_mode(self):
        """
        If set to False, CORS will opperate in the 'old' way, otherwise
        CORS works more strictly according to the spec.
        """
        return self.get_boolean('strict_cors_mode', True)

    @property
    def bulk_delete_max_count(self):
        """
        The max number of objects bulk delete can delete.
        """
        return int(self.get('bulk_delete_max_count', 1000))

    @property
    def object_deletion_wait_interval(self):
        """
        Interval in seconds to wait for x_delete_at
        """
        return int(self.get('object_deletion_wait_interval', '70'))

    @property
    def max_retry_count(self):
        """
        The maximum number of retries the retry_until_success method will
        run.
        """
        return int(self.get('max_retry_count', '5'))

    @property
    def retry_sleep_time(self):
        """
        The amount of time, in seconds, that the retry_until_success method
        will wait between retries.
        """
        return int(self.get('retry_sleep_time', '5'))

    @property
    def cleanup_failure_container_name(self):
        """
        The container name that will store clean up failure logs.
        """
        return self.get('cleanup_failure_container_name',
                        'test_cleanup_failures')


class UserAuthConfig(ConfigSectionInterface):

    SECTION_NAME = 'user_auth_config'

    @property
    def auth_endpoint(self):
        """The authentication endpoint to use for the credentials in the
        [user] config section.  This value is used by the auth provider.
        """

        return self.get("endpoint")

    @property
    def strategy(self):
        """The type of authentication exposed by the auth_endpoint. Currently,
        supported values are 'keystone', 'rax_auth', 'rax_auth_mfa', or
        'saio_tempauth'.
        """
        return self.get("strategy")


class UserConfig(ConfigSectionInterface):

    SECTION_NAME = 'user'

    @property
    def username(self):
        """The name of the user, if applicable"""
        return self.get("username")

    @property
    def api_key(self):
        """The user's api key, if applicable"""
        return self.get_raw("api_key")

    @property
    def password(self):
        """The user's password, if applicable"""
        return self.get_raw("password")

    @property
    def tenant_id(self):
        """The user's tenant_id, if applicable"""
        return self.get("tenant_id")

    @property
    def tenant_name(self):
        """The user's tenant_name, if applicable"""
        return self.get("tenant_name")

    @property
    def user_id(self):
        """The users's user_id, if applicable"""
        return self.get("user_id")

    @property
    def project_id(self):
        """The users's project_id, if applicable"""
        return self.get("project_id")

    @property
    def passcode(self):
        """The auth MFA's secondary password/passcode"""
        return self.get("passcode", 'MFA_PASSCODE_NOT_SET')
