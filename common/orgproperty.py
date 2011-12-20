# -*- coding: utf-8 -*-
# Time-stamp: <2011-12-20 15:13:31 awieser>
from common.orgformat import OrgFormat
import time


class OrgProperties(object):
    """
    Class for handling Memacs's org-drawer:

    :PROPERTIES:
    ...
    :CREATED: <timestamp>
    :<tag>: value
    ...
    :END:

    if no property with tag "CREATED" is added,
    a default one will be added with current timestamp
    """

    def __init__(self):
        """
        Ctor
        """
        self.__properties = []

    def __has_property(self, tag):
        """
        Checks if we have a property with a given tag

        @param tag: tag search for
        @return: True - if tag was found
                 False - Otherwise
        """
        has_tag = False
        for p in self.__properties:
            if p.get_tag() == tag:
                return True
        return False

    def add(self, org_property):
        """
        Add an OrgProperty object to the properties
        """
        assert type(org_property) == OrgProperty
        self.__properties.append(org_property)

    def add_property(self, tag, value):
        """
        Add an OrgProperty(tag,value) to the properties
        @param tag: property tag
        @param value: property value
        """
        self.__properties.append(OrgProperty(tag, value))

    def __unicode__(self):
        """
        for representig properties in unicode with org formatting
        """
        if not self.__has_property("CREATED"):
            self.add(OrgProperty("CREATED",
                                 OrgFormat.datetime(time.localtime())))
        ret = unicode(OrgProperty("PROPERTIES"))
        for p in self.__properties:
            ret += unicode(p)
        ret += unicode(OrgProperty("END"))
        return ret


class OrgProperty(object):
    """
    Class for representing one Property:
    i.e.:
    :DESCRIPTION: foo
    :<tag>: <value>
    """

    def __init__(self, tag, value=u""):
        """
        Ctor
        """
        self.__tag = tag
        self.__value = value

    def __unicode__(self):
        """
        for representig property in unicode with org formatting
        """
        return u"  :" + unicode(self.__tag) + u": " + \
            unicode(self.__value) + u"\n"

    def get_tag(self):
        """
        @param return: tag
        """
        return self.__tag

    def get_value(self):
        """
        @param return: value
        """
        return self.__value
