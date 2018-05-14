from data_interfaces import (
    ConfigSectionInterface, _get_path_from_env)


class DriverConfig(ConfigSectionInterface):
    """
    Unittest driver configuration values.

    This config section is intended to supply values and configuration that can
    not be programatically identified to the unittest driver.
    """

    SECTION_NAME = 'drivers.unittest'

    def __init__(self, config_file_path=None):
        config_file_path = config_file_path or _get_path_from_env(
            'CAFE_ENGINE_CONFIG_FILE_PATH')
        super(DriverConfig, self).__init__(config_file_path=config_file_path)

    @property
    def ignore_empty_datasets(self):
        """
        Identify whether empty datasets should change suite results.

        A dataset provided to a suite should result in the suite failing. This
        value provides a mechanism to modify that behavior in the case of
        suites with intensionally included empty datasets. If this is set to
        'True' empty datasets will not cause suite failures. This defaults
        to 'False'.
        """
        return self.get_boolean(
            item_name="ignore_empty_datasets",
            default=False)
