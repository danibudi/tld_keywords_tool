#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from namecheap_api import namecheap_domains_check

domains = [u'alabaladomain.com', u'раббота.com', u'труд.com' ,u'availabledomain.com', u'google.com']

class TestApi(unittest.TestCase):
    def test_get_HTTPResponce(self):
        domains_status, err = namecheap_domains_check(domain_list=domains)
        self.assertEquals(domains_status,
                          {'google.com': False, #'vintech.com': 'false',
                           'availabledomain.com': False, u'раббота.com': True, u'труд.com': True,
                           'alabaladomain.com': True})
        domains_status, err = namecheap_domains_check()
        self.assertEquals(domains_status, {})
        domains_status, err = namecheap_domains_check('dummy')
        self.assertEquals(domains_status, {})


if __name__ == '__main__':
    unittest.main()
