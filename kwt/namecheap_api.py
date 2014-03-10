# -*- coding: utf-8 -*-
import urllib
import urllib2
import xml.etree.ElementTree as ET

from settings import api_key, api_user, command, user_name, clientIp, url


def namecheap_domains_check(domain_list=[]):
    domains_status = {}
    err = ''
    if not domain_list:
        return domains_status, err
    domains_idna = ','.join(dom.encode('idna') for dom in domain_list)
    data = {}
    data['DomainList'] = domains_idna
    data['ApiUser'] = api_user
    data['UserName'] = user_name
    data['ApiKey'] = api_key
    data['Command'] = command
    data['ClientIp'] = clientIp
    url_values = urllib.urlencode(data)
    full_url = url + '?' + url_values
    data = urllib2.urlopen(full_url)
    the_page = data.read()
    root = ET.fromstring(the_page)
    if root.iter('Errors'):
        for e in root.iter('{http://api.namecheap.com/xml.response}Error'):
            try:
                err = err + e.text + '; '  # .split("Provider for tld '")[1][:3].strip("'")
            except:
                err_c = e.text
                if (domains_status != {}) and err_c == 'Parameter DomainList is Missing':
                    err = err + err_c + '; '
    for domain in root.iter('{http://api.namecheap.com/xml.response}DomainCheckResult'):
        b = (domain.attrib['Available'] == 'true')
        domains_status[unicode(domain.attrib['Domain'], 'idna')] = b
    return (domains_status, err)
