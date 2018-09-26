import hmac
import requests
import tarfile
import urllib
from cStringIO import StringIO
from datetime import datetime
from hashlib import sha1, sha256
from os.path import expanduser
from time import time, mktime
from urlparse import urlparse

from snappy.tools import randomstring as randstring
from snappy.tools.md5hash import get_md5_hash

from responses import AccountContainersList, ContainerObjectsList
from snappy.common.deserialization_decorator import deserialize

BULK_ARCHIVE_NAME = 'bulk_objects'


class ObjectStorageAPIClient(object):
    def __init__(self, storage_url, auth_token, base_container_name=None,
                 base_object_name=None):
        super(ObjectStorageAPIClient, self).__init__()

        # This should be passed in instead of being instantiated on its own
        # self.engine_config = EngineConfig()
        # self.temp_dir = expanduser(self.engine_config.temp_directory)

        # Temp hack
        self.temp_dir = expanduser('~/.temp')

        self.swift_endpoint = storage_url.split('/v1/')[0]
        self.storage_url = storage_url
        self.auth_token = auth_token
        self.base_container_name = base_container_name or ''
        self.base_object_name = base_object_name or ''

        self.default_headers = {
            'X-Auth-Token': self.auth_token,
            'Content-type': 'application/json',
        }
        self._swift_features = None

    def request(
            self, method, url, headers=None, params=None, data=None,
            requestslib_kwargs=None):

        # set requestslib_kwargs to an empty dict if None
        requestslib_kwargs = requestslib_kwargs if (
            requestslib_kwargs is not None) else {}

        # Set defaults
        params = params if params is not None else {}
        verify = False

        # If headers are provided by both, headers "wins" over default_headers
        headers = dict(self.default_headers, **(headers or {}))
        for header in headers:
            if not isinstance(headers[header], str):
                headers[header] = str(headers[header])

        # Override url if present in requestslib_kwargs
        if 'url' in requestslib_kwargs.keys():
            url = requestslib_kwargs.get('url', None) or url
            del requestslib_kwargs['url']

        # Override method if present in requestslib_kwargs
        if 'method' in requestslib_kwargs.keys():
            method = requestslib_kwargs.get('method', None) or method
            del requestslib_kwargs['method']

        # The requests lib already removes None key/value pairs, but we
        # force it here in case that behavior ever changes
        for key in requestslib_kwargs.keys():
            if requestslib_kwargs[key] is None:
                del requestslib_kwargs[key]

        # Create the final parameters for the call to the base request()
        # Wherever a parameter is provided both by the calling method AND
        # the requests_lib kwargs dictionary, requestslib_kwargs "wins"
        requestslib_kwargs = dict({'headers': headers,
                                   'params': params,
                                   'verify': verify,
                                   'data': data},
                                  **requestslib_kwargs)

        # Make the request
        return requests.request(method, url, **requestslib_kwargs)

    def put(self, url, **kwargs):
        """ HTTP PUT request """
        return self.request('PUT', url, **kwargs)

    def copy(self, url, **kwargs):
        """ HTTP COPY request """
        return self.request('COPY', url, **kwargs)

    def post(self, url, data=None, **kwargs):
        """ HTTP POST request """
        return self.request('POST', url, data=data, **kwargs)

    def get(self, url, **kwargs):
        """ HTTP GET request """
        return self.request('GET', url, **kwargs)

    def head(self, url, **kwargs):
        """ HTTP HEAD request """
        return self.request('HEAD', url, **kwargs)

    def delete(self, url, **kwargs):
        """ HTTP DELETE request """
        return self.request('DELETE', url, **kwargs)

    def options(self, url, **kwargs):
        """ HTTP OPTIONS request """
        return self.request('OPTIONS', url, **kwargs)

    def get_swift_info(self, headers=None, params=None,
                       requestslib_kwargs=None):
        """
        Returns Swift info.

        @param headers: headers to be added to the HTTP request.
        @type  headers: dictionary
        @param params: query string parameters to be added to the HTTP request.
        @type  params: dictionary
        @param requestslib_kwargs: keyword arguments to be passed on to
                                   python requests.
        @type requestslib_kwargs: dictionary

        @return: Swift info
        @rtype: response object
        """
        info_url = '{0}/info'.format(self.swift_endpoint)
        return self.get(info_url,
                        headers=headers,
                        params=params,
                        requestslib_kwargs=requestslib_kwargs)

    def health_check(self, headers=None, params=None,
                     requestslib_kwargs=None):
        """
        Returns Health Check.

        @param headers: headers to be added to the HTTP request.
        @type  headers: dictionary
        @param params: query string parameters to be added to the HTTP request.
        @type  params: dictionary
        @param requestslib_kwargs: keyword arguments to be passed on to
                                   python requests.
        @type requestslib_kwargs: dictionary

        @return: response object
        @rtype: object
        """
        parsed_url = urlparse(self.storage_url)
        health_url = "{0}://{1}/healthcheck".format(
            parsed_url.scheme,
            parsed_url.netloc)

        return self.get(health_url,
                        headers=headers,
                        params=params,
                        requestslib_kwargs=requestslib_kwargs)

    # Account----------------------------------------------------------------

    def get_account_metadata(self):
        response = self.head(self.storage_url)

        return response

    @deserialize(AccountContainersList)
    def list_containers(self, headers=None, params=None,
                        requestslib_kwargs=None):
        """
        Lists all containers for the account.

        If the 'format' variable is passed as part of the 'params'
        dictionary, an object representing the deserialized version of
        that format (either xml or json) will be appended to the response
        as the 'entity' attribute. (ie, response.entity)

        @param headers: headers to be added to the HTTP request.
        @type headers: dictionary
        @param params: query string parameters to be added to the HTTP request.
        @type params: dictionary
        @param requestslib_kwargs: keyword arguments to be passed on to
                                   python requests.
        @type requestslib_kwargs: dictionary

        @return: response object
        @rtype: object
        """
        response = self.get(
            self.storage_url,
            headers=headers,
            params=params,
            requestslib_kwargs=requestslib_kwargs)

        return response

    # Container--------------------------------------------------------------

    def get_container_metadata(self, container_name, headers=None,
                               requestslib_kwargs=None):
        url = '{0}/{1}'.format(self.storage_url, container_name)

        response = self.head(
            url,
            headers=headers,
            requestslib_kwargs=requestslib_kwargs)

        return response

    def create_container(self, container_name, headers=None,
                         requestslib_kwargs=None):
        url = '{0}/{1}'.format(self.storage_url, container_name)

        response = self.put(
            url,
            headers=headers,
            requestslib_kwargs=requestslib_kwargs)

        return response

    def delete_container(self, container_name, headers=None,
                         requestslib_kwargs=None):
        url = '{0}/{1}'.format(self.storage_url, container_name)

        response = self.delete(
            url,
            headers=headers,
            requestslib_kwargs=requestslib_kwargs)

        return response

    def set_container_metadata(self, container_name, headers=None,
                               requestslib_kwargs=None):
        url = '{0}/{1}'.format(self.storage_url, container_name)

        response = self.post(
            url,
            headers=headers,
            requestslib_kwargs=requestslib_kwargs)

        return response

    def get_container_options(self, container_name, headers=None,
                              requestslib_kwargs=None):
        """
        returns response from CORS option call
        """
        url = '{0}/{1}'.format(self.storage_url, container_name)

        response = self.options(
            url,
            headers=headers,
            requestslib_kwargs=requestslib_kwargs)

        return response

    @deserialize(ContainerObjectsList)
    def list_objects(self, container_name, headers=None, params=None,
                     requestslib_kwargs=None):
        """
        Lists all objects in the specified container.

        If the 'format' variable is passed as part of the 'params'
        dictionary, an object representing the deserialized version of
        that format (either xml or json) will be appended to the response
        as the 'entity' attribute. (ie, response.entity)

        @param container_name: container to list the object from.
        @type container_name: string
        @param headers: headers to be added to the HTTP request.
        @type headers: dictionary
        @param params: query string parameters to be added to the HTTP request.
        @type params: dictionary
        @param requestslib_kwargs: keyword arguments to be passed on to
                                   python requests.
        @type requestslib_kwargs: dictionary

        @return: response object
        @rtype: object
        """
        url = '{0}/{1}'.format(self.storage_url, container_name)

        response = self.get(
            url,
            headers=headers,
            params=params,
            requestslib_kwargs=requestslib_kwargs)

        return response

    # Storage Object--------------------------------------------------------

    def get_object(self, container_name, object_name, headers=None,
                   params=None, stream=False,
                   requestslib_kwargs=None):
        """
        optional headers

        If-Match
        If-None-Match
        If-Modified-Since
        If-Unmodified-Since
        Range

        If-Match and If-None-Match check the ETag header
        200 on 'If' header success
        If none of the entity tags match, or if "*" is given and no current
        entity exists, the server MUST NOT perform the requested method, and
        MUST return a 412 (Precondition Failed) response.

        206 (Partial content) for successful range request
        If the entity tag does not match, then the server SHOULD
        return the entire entity using a 200 (OK) response
        see RFC2616

        If prefetch=False, body download is delayed until response.content is
        accessed either directly, via response.iter_content() or .iter_lines()
        """
        url = '{0}/{1}/{2}'.format(
            self.storage_url,
            container_name,
            object_name)

        response = self.get(
            url,
            headers=headers,
            params=params,
            requestslib_kwargs={'stream': stream})

        return response

    def create_object(self, container_name, object_name, data=None,
                      headers=None, params=None,
                      requestslib_kwargs=None):
        """
        Creates a storage object in a container via PUT
        """
        url = '{0}/{1}/{2}'.format(
            self.storage_url,
            container_name,
            object_name)

        response = self.put(
            url,
            data=data,
            headers=headers,
            params=params,
            requestslib_kwargs=requestslib_kwargs)

        return response

    def create_archive_object(self, data, extract_archive_param,
                              upload_path='', headers=None,
                              requestslib_kwargs=None):
        """
        Extracts an archive to object(s) via PUT to the storage url
        extract-archive param formats: tar, tar.gz, tar.bz2
        upload_path notes:
        given an archive:

        archive
          file1/name1
          file2/name2
          file3
          file4

        if no upload path is given then the filenames in the archive
        will be extracted to container file1 with obj name1,
        container file2 with obj name2, etc. and obj names without
        slashes will be ignored.

        if the upload path is 'container_foo' all the objects will be
        extracted to 'container_foo' with obj names file1/name1,
        file2/name2, file3...file_n

        if the upload path is container_foo/bar then the objects will
        be extracted to container_foo with the obj name prefix of 'bar'
        ie bar/file1/name1, bar/file2/name2, bar/file3...bar/file_n
        """
        url = '{0}/{1}'.format(
            self.storage_url,
            upload_path)

        params = {"extract-archive": extract_archive_param}

        response = self.put(
            url,
            data=data,
            headers=headers,
            params=params,
            requestslib_kwargs=requestslib_kwargs)

        return response

    def copy_object(self, container_name, object_name, headers=None,
                    requestslib_kwargs=None):
        url = '{0}/{1}/{2}'.format(
            self.storage_url,
            container_name,
            object_name)

        if 'X-Copy-From' in headers:
            method = 'PUT'
            if 'Content-Length' not in headers:
                headers['Content-Length'] = '0'
        elif 'Destination' in headers:
            method = 'COPY'
        else:
            return None

        response = self.request(
            method=method,
            url=url,
            headers=headers,
            requestslib_kwargs=requestslib_kwargs)

        return response

    def delete_object(self, container_name, object_name, headers=None,
                      requestslib_kwargs=None):
        url = '{0}/{1}/{2}'.format(
            self.storage_url,
            container_name,
            object_name)

        response = self.delete(
            url,
            headers=headers,
            requestslib_kwargs=requestslib_kwargs)

        return response

    def get_object_metadata(self, container_name, object_name, headers=None,
                            requestslib_kwargs=None):
        url = '{0}/{1}/{2}'.format(
            self.storage_url,
            container_name,
            object_name)

        response = self.head(
            url,
            headers=headers,
            requestslib_kwargs=requestslib_kwargs)

        return response

    def set_object_metadata(self, container_name, object_name, headers,
                            requestslib_kwargs=None):
        url = '{0}/{1}/{2}'.format(
            self.storage_url,
            container_name,
            object_name)

        response = self.post(
            url,
            headers=headers,
            requestslib_kwargs=requestslib_kwargs)

        return response

    def set_temp_url_key(self, container_name=None, headers=None,
                         requestslib_kwargs=None):
        """
        optional container name is for setting the tempurl at the container
        level, otherwise key is set at the account level.
        """
        url = self.storage_url

        if container_name:
            url = "{0}/{1}".format(self.storage_url, container_name)

        response = self.post(
            url,
            headers=headers,
            requestslib_kwargs=requestslib_kwargs)

        return response

    def create_temp_url(self, method, container, obj, seconds, key,
                        sha_type=None):
        method = method.upper()
        base_url = '{0}/{1}/{2}'.format(self.storage_url, container, obj)
        account_hash = self.storage_url.split('/v1/')[1]
        object_path = '/v1/{0}/{1}/{2}'.format(account_hash, container, obj)
        seconds = int(seconds)
        expires = int(time() + seconds)
        hmac_body = '{0}\n{1}\n{2}'.format(method, expires, object_path)
        if sha_type == 'sha2':
            sig = hmac.new(key, hmac_body, sha256).hexdigest()
        else:
            sig = hmac.new(key, hmac_body, sha1).hexdigest()

        return {'target_url': base_url, 'signature': sig, 'expires': expires}

    def create_archive(self, object_names, compression_type,
                       archive_name=BULK_ARCHIVE_NAME):
        """
        Bulk creates objects in the opencafe's temp directory specified in the
        engine config. Each object's data will be the md5sum of the object's
        name.

        @type  object_names: strings
        @param object_names: a list of object names

        @type  object_names: string
        @param object_names: file compression to apply to the archive

        @rtype:  string
        @return: Returns full path of the archive that was created in
        opencafe's temp directory specified in the engine config
        """
        supported = [None, "gz", "bz2"]
        if compression_type not in supported:
            raise NameError("supported compression: {0}".format(supported))

        ext = ''

        if not compression_type:
            ext = 'tar'
            compression_type = ''
        else:
            ext = 'tar.{0}'.format(compression_type)

        archive_name = '{0}_{1}.{2}'.format(
            archive_name,
            randstring.get_random_string(),
            ext)

        archive_filename = '{0}/{1}'.format(self.temp_dir, archive_name)
        archive = tarfile.open(
            archive_filename,
            'w:{0}'.format(compression_type))

        for object_name in object_names:
            object_data = get_md5_hash(object_name)
            object_size = len(object_data)
            object_time = int(mktime(datetime.now().timetuple()))

            object_buffer = StringIO(object_data)
            object_buffer.seek(0)

            object_info = tarfile.TarInfo(name=object_name)
            object_info.size = object_size
            object_info.mtime = object_time

            archive.addfile(tarinfo=object_info, fileobj=object_buffer)
        archive.close()

        archive_path = "{0}/{1}".format(
            self.temp_dir,
            archive_name)

        return archive_path

    def bulk_delete(self, targets, headers=None, requestslib_kwargs=None):
        """
        Deletes container/objects from an account.

        @type  targets: list of strings
        @param targets: A list of the '/container/object' or '/container'
            to be bulk deleted.  Note, bulk delete will not remove
            containers that have objects in them, and there is limit of
            1000 containers/objects per delete.

        @rtype:  object
        @return: The requests response object returned from the call.
        """
        if not headers:
            headers = {}
        url = '{0}{1}'.format(self.storage_url, '?bulk-delete')
        data = '\n'.join([urllib.quote(target) for target in targets])
        headers['content-type'] = 'text/plain'
        headers['content-length'] = str(len(data))

        response = self.request(
            'DELETE', url, data=data, headers=headers,
            requestslib_kwargs=requestslib_kwargs)

        return response
