# -*- coding: utf-8 -*-
# Time-stamp: <2011-12-20 15:13:31 awieser>
from common.orgformat import OrgFormat
import time


class OrgProperties(object):

    def __init__(self):
        self.__properties = []

    def __has_property(self, tag):
        """
        TODO: document this
        """
        has_tag = False
        for p in self.__properties:
            if p.get_tag() == tag:
                return True
        return False

    def add(self, org_property):
        assert type(org_property) == OrgProperty
        self.__properties.append(org_property)

    def add_property(self, tag, value):
        self.__properties.append(OrgProperty(tag, value))

    def __unicode__(self):
        if not self.__has_property("CREATED"):
            self.add(OrgProperty("CREATED",
                                 OrgFormat.datetime(time.localtime())))
        ret = unicode(OrgProperty("PROPERTIES"))
        for p in self.__properties:
            ret += unicode(p)
        ret += unicode(OrgProperty("END"))
        return ret


class OrgProperty(object):
    def __init__(self, tag, value=u""):
        self.__tag = tag
        self.__value = value

    def __unicode__(self):
        return u"  :" + unicode(self.__tag) + u": " + \
            unicode(self.__value) + u"\n"

    def get_tag(self):
        return self.__tag

    def get_value(self):
        return self.__value
