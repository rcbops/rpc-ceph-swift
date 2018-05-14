class Constants(object):

    VALID_OBJECT_NAME = 'object'
    VALID_OBJECT_NAME_WITH_SLASH = 'object/foo'
    VALID_OBJECT_NAME_WITH_TRAILING_SLASH = 'object/'
    VALID_OBJECT_DATA = 'object data.'
    VALID_OBJECT_NAME_WITH_UNICODE = u'object_{0}'.format(
        unicode(u'\u262D\u2622')).encode('utf-8')

    BASE_TEMPURL_KEY = 'qe-tempurl-key'