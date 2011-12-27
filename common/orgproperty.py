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
        self.__properties = {}

    def add(self, tag, value):
        """
        Add an OrgProperty(tag,value) to the properties
        @param tag: property tag
        @param value: property value
        """
        self.__properties[tag.upper()] = unicode(value)

    def __get_property_max_tag_width(self):
        width = 7  # :PROPERTIES: has width 7
        for key in self.__properties.keys():
            if width < len(key):
                width = len(key)
        return width

    def __format_tag(self, tag):
        num_whitespaces = self.__get_property_max_tag_width() - len(tag)
        whitespaces = ""
        for w in range(num_whitespaces):
            whitespaces += " "
        return "   :" + tag + ": " + whitespaces

    def __unicode__(self):
        """
        for representig properties in unicode with org formatting
        """
        if "CREATED" not in self.__properties:
            self.add("CREATED",
                     OrgFormat.inactive_datetime(time.localtime()))
        ret = "   :PROPERTIES:\n"

        for tag, value in self.__properties.iteritems():
            ret += self.__format_tag(tag) + value + "\n"

        ret += "   :END:"
        return ret

    def get_value(self, key):
        """
        @return: properties[key]
        """
        return self.__properties[key]
