# -*- coding: utf-8 -*-
# Time-stamp: <2012-03-09 14:39:17 armin>
import hashlib


class OrgProperties(object):
    """
    Class for handling Memacs's org-drawer:

    :PROPERTIES:
    ...
    :<tag>: value
    ...
    :ID:  - id is generated from all above tags/values
    :END:
    """

    def __init__(self, data_for_hashing=""):
        """
        Ctor
        @param data_for_hashing: if no special properties are set,
        you can add here data only for hash generation
        """
        self.__properties = {}
        self.__data_for_hashing = data_for_hashing
        self.__id = None

    def add(self, tag, value):
        """
        Add an OrgProperty(tag,value) to the properties
        @param tag: property tag
        @param value: property value
        """
        tag = unicode(tag).strip().upper()
        value = unicode(value).strip()
        if tag == "ID":
            raise Exception("you should not specify an :ID: property " + \
                            "it will be generated automatically")

        self.__properties[tag] = unicode(value)

    def set_id(self, value):
        """
        set id here, then its not generated / hashed
        """
        self.__id = value

    def delete(self, key):
        """
        delete a pair out of properties
        @param key index
        """
        del self.__properties[key]

    def __get_property_max_tag_width(self):
        width = 10  # :PROPERTIES: has width 10
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

        if self.__properties == {} and \
            self.__data_for_hashing == "" and \
            self.__id == None:
            raise Exception("No data for hashing specified,  and no " + \
                            "property was given. Cannot generate unique ID.")

        ret = "   :PROPERTIES:\n"

        for tag, value in self.__properties.iteritems():
            ret += self.__format_tag(tag) + value + "\n"

        ret += self.__format_tag("ID") + self.get_id() + "\n"
        ret += "   :END:"
        return ret

    def get_id(self):
        """
        generates the hash string for all properties
        @return: sha1(properties)
        """
        if self.__id != None:
            return self.__id
        to_hash = "".join(map(unicode, self.__properties.values()))
        to_hash += "".join(map(unicode, self.__properties.keys()))
        to_hash += self.__data_for_hashing
        return hashlib.sha1(to_hash.encode('utf-8')).hexdigest()

    def get_value(self, key):
        """
        @param: key of property
        @return: returns the value of a given key
        """
        return self.__properties[key]

    def add_data_for_hashing(self, data_for_hashing):
        """
        add additional data for hashing
        useful when no possibility to set in Ctor
        """
        self.__data_for_hashing += data_for_hashing

    def get_value_delete_but_add_for_hashing(self, key):
        """
        see method name ;)
        """
        ret = self.get_value(key)
        self.delete(key)
        self.add_data_for_hashing(ret)
        return ret
