
class OrgFormat(object):
    
    @staticmethod
    def link(link, description=None):
        """
        returns a link in org-format
        @param link link to i.e. file
        @param description optional  
        """
        
        link = link.replace(" ", "%20")
        
        if description:
            return u"[[" + link + u"][" + description + u"]]"
        else:
            return u"[[" + link + u"]]"
    
    @staticmethod
    def date(year,month,day,hour,minute):
        # <YYYY-MM-DD hh:mm>
        
        
        return u"<%s-%s-%s %s:%s>" % (year,month,day,hour,minute)
        #return u"<""> "
        