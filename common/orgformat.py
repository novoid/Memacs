#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2011-11-02 15:13:31 aw>

import time

class OrgFormat(object):
    
    @staticmethod
    def link(link, description=None):
        """
        returns string of a link in org-format
        @param link link to i.e. file
        @param description optional  
        """
        
        link = link.replace(" ", "%20")
        
        if description:
            return u"[[" + link + u"][" + description + u"]]"
        else:
            return u"[[" + link + u"]]"
    
    @staticmethod
    def date(tuple_date, show_time=False):
        """
        returns a date string in org format
        i.e.: * <YYYY-MM-DD Sun>        
              * <YYYY-MM-DD Sun HH:MM>
        @param tuple_date: has to be a time.struct_time
        @param show_time: optional show time also
        """
        # <YYYY-MM-DD hh:mm>
        assert tuple_date.__class__ == time.struct_time

        if show_time:
            if tuple_date.tm_sec == 0:
                return time.strftime("<%Y-%m-%d %a %H:%M>", tuple_date)
            else:
                return time.strftime("<%Y-%m-%d %a %H:%M:%S>", tuple_date)
        else:
            return time.strftime("<%Y-%m-%d %a>", tuple_date)
    
    @staticmethod
    def datetime(tuple_datetime):
        """
        returns a date+time string in org format
        wrapper for OrgFormat.date(show_time=True)
        
        @param tuple_datetime has to be a time.struct_time 
        """
        return OrgFormat.date(tuple_datetime, show_time=True)
    
    @staticmethod
    def strdate(date_string):
        """
        returns a date string in org format
        i.e.: * <YYYY-MM-DD Sun>        
        @param date-string: has to be a str in following format:  YYYY-MM-DD
        """
        assert date_string.__class__ == str
        tuple_date = OrgFormat.datetupeliso8601(date_string)
        return OrgFormat.date(tuple_date, show_time=False)
        
    @staticmethod
    def strdatetime(datetime_string):
        """
        returns a date string in org format
        i.e.: * <YYYY-MM-DD Sun HH:MM>
        @param date-string: has to be a str in following format: YYYY-MM-DD HH:MM
        """
        assert datetime_string.__class__ == str
        tuple_date = time.strptime(datetime_string, "%Y-%m-%d %H:%M")
        return OrgFormat.date(tuple_date,show_time=True)
    
    @staticmethod
    def strdatetimeiso8601(datetime_string):
        """
        returns a date string in org format
        i.e.: * <YYYY-MM-DD Sun HH:MM>
        @param date-string: has to be a str in following format: YYYY-MM-DDTHH.MM.SS or
                                                                 YYYY-MM-DDTHH.MM  
        """
        assert datetime_string.__class__ == str
        tuple_date = OrgFormat.datetimetupeliso8601(datetime_string)
        return OrgFormat.date(tuple_date,show_time=True)
        
    @staticmethod
    def datetimetupeliso8601(datetime_string):
        assert datetime_string.__class__ == str
        try:
            return time.strptime(datetime_string, "%Y-%m-%dT%H.%M.%S")
        except ValueError:
            return time.strptime(datetime_string, "%Y-%m-%dT%H.%M")
        
    @staticmethod
    def datetupeliso8601(datetime_string):
        assert datetime_string.__class__ == str
        return time.strptime(datetime_string, "%Y-%m-%d")