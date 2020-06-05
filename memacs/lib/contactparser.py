import logging
import re


def parse_org_contact_file(orgfile):
    """
    Parses the given Org-mode file for contact entries.

    The return format is a follows:
    numbers = {'004369912345678':'First2 Last1', '0316987654':'First2 Last2', ...}

    @param orgfile: file name of a Org-mode file to parse
    @param return: list of dict-entries containing the numbers to name dict
    """

    linenr = 0

    ## defining distinct parsing status states:
    headersearch = 21
    propertysearch = 42
    inproperty = 73
    status = headersearch

    contacts = {}
    current_name = ''

    HEADER_REGEX = re.compile('^(\*+)\s+(.*?)(\s+(:\S+:)+)?$')
    PHONE = '\s+([\+\d\-/ ]{7,})$'
    PHONE_REGEX = re.compile(':(PHONE|oldPHONE|MOBILE|oldMOBILE|HOMEPHONE|oldHOMEPHONE|WORKPHONE|oldWORKPHONE):' + PHONE)

    for rawline in open(orgfile, 'r'):
        line = rawline.strip()   ## trailing and leading spaces are stupid
        linenr += 1

        header_components = re.match(HEADER_REGEX, line)
        if header_components:
            ## in case of new header, make new currententry because previous one was not a contact header with a property
            current_name = header_components.group(2)
            status = propertysearch
            continue

        if status == headersearch:
            ## if there is something to do, it was done above when a new heading is found
            continue

        if status == propertysearch:
            if line == ':PROPERTIES:':
                status = inproperty
            continue

        elif status == inproperty:

            phone_components = re.match(PHONE_REGEX, line)
            if phone_components:
                phonenumber = phone_components.group(2).strip().replace('-','').replace('/','').replace(' ','').replace('+','00')
                contacts[phonenumber] = current_name
            elif line == ':END:':
                status = headersearch

            continue

        else:
            ## I must have mixed up status numbers or similar - should never be reached.
            logging.error("Oops. Internal parser error: status \"%s\" unknown. The programmer is an idiot. Current contact entry might get lost due to recovering from that shock. (line number %s)" % (str(status), str(linenr)))
            status = headersearch
            continue

    logging.info("found %s suitable contacts while parsing \"%s\"" % (str(len(contacts)), orgfile))
    return contacts
