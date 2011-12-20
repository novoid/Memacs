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
            if p.tag == tag:
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

    def __get_property_max_tag_width(self):
        width = 7
        for p in self.__properties:
            if width < len(p.tag):
                width = len(p.tag)
        return width

    def __format_tag(self,tag):
        num_whitespaces = self.__get_property_max_tag_width() - len(tag)
        whitespaces = ""
        for w in range(num_whitespaces):
            whitespaces += " "
        return "  :" + tag +": " + whitespaces


    def __unicode__(self):
        """
        for representig properties in unicode with org formatting
        """
        if not self.__has_property("CREATED"):
            self.add(OrgProperty("CREATED",
                                 OrgFormat.inactive_datetime(time.localtime())))
        ret = "  :PROPERTIES:\n"

        for p in self.__properties:
            ret += self.__format_tag(p.tag) + p.value + "\n"

        ret += "  :END:"
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
        self.tag = tag.strip()
        self.value = value.strip()

