import cclogging
import six


class BaseModel(object):
    __REPR_SEPARATOR__ = '\n'

    def __init__(self):
        self._log = cclogging.getLogger(
            cclogging.get_object_namespace(self.__class__))

    def __eq__(self, obj):
        try:
            if vars(obj) == vars(self):
                return True
        except:
            pass

        return False

    def __ne__(self, obj):
        return not self.__eq__(obj)

    def __str__(self):
        strng = '<{0} object> {1}'.format(
            type(self).__name__, self.__REPR_SEPARATOR__)
        for key in list(vars(self).keys()):
            val = getattr(self, key)
            if isinstance(val, cclogging.logging.Logger):
                continue
            elif isinstance(val, six.text_type):
                strng = '{0}{1} = {2}{3}'.format(
                    strng, key, val.encode("utf-8"), self.__REPR_SEPARATOR__)
            else:
                strng = '{0}{1} = {2}{3}'.format(
                    strng, key, val, self.__REPR_SEPARATOR__)
        return '{0}'.format(strng)

    def __repr__(self):
        return self.__str__()


class AutoMarshallingModel(BaseModel):
    """
    @summary: A class used as a base to build and contain the logic necessary
             to automatically create serialized requests and automatically
             deserialize responses in a format-agnostic way.
    """
    _log = cclogging.getLogger(__name__)

    def __init__(self):
        super(AutoMarshallingModel, self).__init__()
        self._log = cclogging.getLogger(
            cclogging.get_object_namespace(self.__class__))

    def serialize(self, format_type):
        serialization_exception = None
        try:
            serialize_method = '_obj_to_{0}'.format(format_type)
            return getattr(self, serialize_method)()
        except Exception as serialization_exception:
            pass

        if serialization_exception:
            try:
                self._log.error(
                    'Error occured during serialization of a data model into'
                    'the "{0}: \n{1}" format'.format(
                        format_type, serialization_exception))
                self._log.exception(serialization_exception)
            except Exception as exception:
                self._log.exception(exception)
                self._log.debug(
                    "Unable to log information regarding the "
                    "deserialization exception due to '{0}'".format(
                        serialization_exception))
        return None

    @classmethod
    def deserialize(cls, serialized_str, format_type):
        cls._log = cclogging.getLogger(
            cclogging.get_object_namespace(cls))

        model_object = None
        deserialization_exception = None
        if serialized_str and len(serialized_str) > 0:
            try:
                deserialize_method = '_{0}_to_obj'.format(format_type)
                model_object = getattr(cls, deserialize_method)(serialized_str)
            except Exception as deserialization_exception:
                cls._log.exception(deserialization_exception)
                pass

        # Try to log string and format_type if deserialization broke
        if deserialization_exception is not None:
            try:
                cls._log.debug(
                    "Deserialization Error: Attempted to deserialize type"
                    " using type: {0}".format(format_type.decode(
                        encoding='UTF-8', errors='ignore')))
                cls._log.debug(
                    "Deserialization Error: Unble to deserialize the "
                    "following:\n{0}".format(serialized_str.decode(
                        encoding='UTF-8', errors='ignore')))
            except Exception as exception:
                cls._log.exception(exception)
                cls._log.debug(
                    "Unable to log information regarding the "
                    "deserialization exception")
        return model_object

    # Serialization Functions
    def _obj_to_json(self):
        raise NotImplementedError

    def _obj_to_xml(self):
        raise NotImplementedError

    # Deserialization Functions
    @classmethod
    def _xml_to_obj(cls, serialized_str):
        raise NotImplementedError

    @classmethod
    def _json_to_obj(cls, serialized_str):
        raise NotImplementedError


class AutoMarshallingListModel(list, AutoMarshallingModel):
    """List-like AutoMarshallingModel used for some special cases"""

    def __str__(self):
        return list.__str__(self)
