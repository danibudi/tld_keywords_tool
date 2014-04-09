# -*- coding: utf-8 -*-
import urllib
import urllib2
import xml.etree.ElementTree as ET

from settings import (api_key, api_user, command, user_name, clientIp, url,
                      amount_of_domains_checked_in_one_API_call,
                      #~ length_of_URL_limited_to
                      )


def parser_data(text=""):
    kw_sv_dict = {}
    for line in text.split('\n'):
        l = line.strip()
        try:
            if '\t' in l:
                kw_sv = l.split('\t')
            else:
                kw_sv = l.split(' ')
            if '' in kw_sv:
                kw_sv.remove('')
        except:
            kw_sv = l.split(' ')
        if kw_sv != ['']:
            try:
                kw_sv_dict[kw_sv[0]] = kw_sv[1]
            except:
                pass
    return kw_sv_dict


def namecheap_domains_check(domain_list=[]):
    """ the exact limit of the amount of the domains that
    can be checked in one API call is 120
    there's a limitation on the string length for GET -
    the length of a URL is limited to 2048 characters maximum.
    https://community.namecheap.com/forums/viewtopic.php?f=17&t=7568"""
    domains_status = {}
    err = ''
    if not domain_list:
        return domains_status, err
    data = {}
    data['ApiUser'] = api_user
    data['UserName'] = user_name
    data['ApiKey'] = api_key
    data['Command'] = command
    data['ClientIp'] = clientIp
    try:
        domainList = [dom.encode('idna') for dom in domain_list]
    except:
        err = UnicodeError("label empty or too long")
        return domains_status, err
    max_amount_domains = amount_of_domains_checked_in_one_API_call
    for i, d in enumerate(range(len(domainList)/max_amount_domains+1)):
        elements_for_namecheap = domainList[
            i*max_amount_domains:(d+1)*max_amount_domains]
        domains = ','.join(i for i in elements_for_namecheap)
        data['DomainList'] = domains
        url_values = urllib.urlencode(data)
        data_url = urllib2.urlopen(url, url_values)
        the_page = data_url.read()
        root = ET.fromstring(the_page)
        if root.iter('Errors'):
            for e in root.iter(
                '{http://api.namecheap.com/xml.response}Error'):
                try:
                    err = err + e.text + '; '  # .split("Provider for tld '")[1][:3].strip("'")
                except:
                    err_c = e.text
                    if (domains_status != {}) and err_c == 'Parameter DomainList is Missing':
                        err = err + err_c + '; '
        for domain in root.iter(
            '{http://api.namecheap.com/xml.response}DomainCheckResult'):
            b = (domain.attrib['Available'] == 'true')
            domains_status[unicode(domain.attrib['Domain'], 'idna')] = b
    return (domains_status, err)
