"""
Copyright 2015 Rackspace

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


class Constants(object):

    VALID_OBJECT_NAME = 'object'
    VALID_OBJECT_NAME_WITH_SLASH = 'object/foo'
    VALID_OBJECT_NAME_WITH_TRAILING_SLASH = 'object/'
    VALID_OBJECT_DATA = 'object data.'
    VALID_OBJECT_NAME_WITH_UNICODE = u'object_{0}'.format(
        unicode(u'\u262D\u2622')).encode('utf-8')

    BASE_TEMPURL_KEY = 'qe-tempurl-key'