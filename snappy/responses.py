import json
from xml.etree import ElementTree


class BaseModel(object):
    __REPR_SEPARATOR__ = '\n'

    def __init__(self):
        # self._log = cclogging.getLogger(
        #     cclogging.get_object_namespace(self.__class__))
        pass

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
        # strng = '<{0} object> {1}'.format(
        #     type(self).__name__, self.__REPR_SEPARATOR__)
        # for key in list(vars(self).keys()):
        #     val = getattr(self, key)
        #     if isinstance(val, cclogging.logging.Logger):
        #         continue
        #     elif isinstance(val, six.text_type):
        #         strng = '{0}{1} = {2}{3}'.format(
        #             strng, key, val.encode("utf-8"), self.__REPR_SEPARATOR__)
        #     else:
        #         strng = '{0}{1} = {2}{3}'.format(
        #             strng, key, val, self.__REPR_SEPARATOR__)
        # return '{0}'.format(strng)
        pass

    def __repr__(self):
        return self.__str__()


class AutoMarshallingModel(BaseModel):
    """
    @summary: A class used as a base to build and contain the logic necessary
             to automatically create serialized requests and automatically
             deserialize responses in a format-agnostic way.
    """

    # _log = cclogging.getLogger(__name__)

    def __init__(self):
        super(AutoMarshallingModel, self).__init__()
        # self._log = cclogging.getLogger(
        #     cclogging.get_object_namespace(self.__class__))

    # def serialize(self, format_type):
    #     serialization_exception = None
    #     try:
    #         serialize_method = '_obj_to_{0}'.format(format_type)
    #         return getattr(self, serialize_method)()
    #     except Exception as serialization_exception:
    #         pass
    #
    #     if serialization_exception:
    #         try:
    #             # self._log.error(
    #             #     'Error occured during serialization of a data model into'
    #             #     'the "{0}: \n{1}" format'.format(
    #             #         format_type, serialization_exception))
    #             # self._log.exception(serialization_exception)
    #             pass
    #         except Exception as exception:
    #             # self._log.exception(exception)
    #             # self._log.debug(
    #             #     "Unable to log information regarding the "
    #             #     "deserialization exception due to '{0}'".format(
    #             #         serialization_exception))
    #             pass
    #     return None

    @classmethod
    def deserialize(cls, serialized_str, format_type):
        # cls._log = cclogging.getLogger(
        #     cclogging.get_object_namespace(cls))

        model_object = None
        deserialization_exception = None
        if serialized_str and len(serialized_str) > 0:
            try:
                deserialize_method = '_{0}_to_obj'.format(format_type)
                model_object = getattr(cls, deserialize_method)(serialized_str)
            except Exception as deserialization_exception:
                # cls._log.exception(deserialization_exception)
                pass

        # Try to log string and format_type if deserialization broke
        if deserialization_exception is not None:
            try:
                # cls._log.debug(
                #     "Deserialization Error: Attempted to deserialize type"
                #     " using type: {0}".format(format_type.decode(
                #         encoding='UTF-8', errors='ignore')))
                # cls._log.debug(
                #     "Deserialization Error: Unble to deserialize the "
                #     "following:\n{0}".format(serialized_str.decode(
                #         encoding='UTF-8', errors='ignore')))
                pass
            except Exception as exception:
                # cls._log.exception(exception)
                # cls._log.debug(
                #     "Unable to log information regarding the "
                #     "deserialization exception")
                pass

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


class StorageObject(object):
    def __init__(self, name, bytes_, hash_, last_modified, content_type):
        self.name = name
        self.bytes_ = bytes_
        self.hash_ = hash_
        self.last_modified = last_modified
        self.content_type = content_type


class Container(object):
    def __init__(self, name=None, count=None, bytes_=None):
        self.name = name
        self.count = count
        self.bytes_ = bytes_


class ArchiveObject(object):
    def __init__(self, num_files_created=None, errors=None, body=None,
                 status=None):
        self.num_files_created = num_files_created
        self.errors = errors
        self.body = body
        self.status = status


class AccountContainersList(AutoMarshallingListModel):

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        root = ElementTree.fromstring(serialized_str)
        data = []
        for child in root:
            account_container_dict = {}
            for sub_child in child:
                account_container_dict[sub_child.tag] = sub_child.text
            data.append(account_container_dict)
        return cls._list_to_obj(data)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        data = json.loads(serialized_str)
        return cls._list_to_obj(data)

    @classmethod
    def _list_to_obj(cls, data):
        account_containers_list = AccountContainersList()
        for obj in data:
            container = Container(
                name=obj.get('name'),
                bytes_=obj.get('bytes'),
                count=obj.get('count'))
            account_containers_list.append(container)
        return account_containers_list

    @classmethod
    def _text_to_obj(cls, data):
        split_data = data.split('\n')

        data_list = [container_name for container_name in split_data
                     if container_name]

        account_containers_list = AccountContainersList()

        for container_name in data_list:
            container = Container(name=container_name)
            account_containers_list.append(container)
        return account_containers_list


class ContainerObjectsList(AutoMarshallingListModel):

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        root = ElementTree.fromstring(serialized_str)
        data = []
        for child in root:
            storage_object_dict = {}
            for sub_child in child:
                storage_object_dict[sub_child.tag] = sub_child.text
            data.append(storage_object_dict)
        return cls._list_to_obj(data)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        data = json.loads(serialized_str)
        return cls._list_to_obj(data)

    @classmethod
    def _list_to_obj(cls, data):
        container_objects_list = ContainerObjectsList()
        for obj in data:
            storage_object = StorageObject(
                name=obj.get('name'),
                bytes_=obj.get('bytes'),
                hash_=obj.get('hash'),
                last_modified=obj.get('last_modified'),
                content_type=obj.get('content_type'))
            container_objects_list.append(storage_object)
        return container_objects_list

    @classmethod
    def _text_to_obj(cls, data):
        split_data = data.split('\n')
        data_list = [obj_name for obj_name in split_data if obj_name]

        container_objects_list = ContainerObjectsList()
        for obj_name in data_list:
            storage_object = StorageObject(
                name=obj_name,
                bytes_=None,
                hash_=None,
                last_modified=None,
                content_type=None)
            container_objects_list.append(storage_object)
        return container_objects_list


class CreateArchiveObject(AutoMarshallingListModel):

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        root = ElementTree.fromstring(serialized_str)
        data = []
        for child in root:
            archive_object_dict = {}
            for sub_child in child:
                archive_object_dict[sub_child.tag] = sub_child.text
            data.append(archive_object_dict)
        return cls._list_to_obj(data)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        data = json.loads(serialized_str)
        return cls._list_to_obj(data)

    @classmethod
    def _list_to_obj(cls, data):
        archive_obj = ArchiveObject(
            num_files_created=data.get("Number Files Created"),
            errors=data.get("Errors"),
            body=data.get("Response Body"),
            status=data.get("Response Status"))
        return archive_obj
