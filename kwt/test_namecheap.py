#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from namecheap_api import namecheap_domains_check, parser_data

domains = [u'alabaladomain.com', u'раббота.com', u'труд.com',
           u'availabledomain.com', u'google.com', 'vintech.bg']


class TestApi(unittest.TestCase):
    def test_get_HTTPResponce(self):
        domains_status, err = namecheap_domains_check(domain_list=domains)
        self.assertEquals(domains_status,
                          {'google.com': False,
                           # 'vintech.bg': Provider for tld 'bg' is not found;
                           'availabledomain.com': False, u'раббота.com': True,
                           u'труд.com': False, 'alabaladomain.com': True})

    def test_get_HTTPResponce_over_NC_limit(self):
        domains_status, err = namecheap_domains_check(
            domain_list=domains*10 + ['conzap.com'])

    def test_get_HTTPResponce_long_domain(self):
        domains_status, err = namecheap_domains_check(
            domain_list=[100*'conzap'+'.com'])
        expected_error = UnicodeError('label empty or too long',)
        self.assertEquals(domains_status, {})
        self.assertRaises(expected_error)

    def test_get_HTTPResponce_over_NC_limit2048_1name(self):
        domains_status, err = namecheap_domains_check(
            domain_list=500*['conzap.com'])
        self.assertEquals(domains_status, {u'conzap.com': False})

    def test_get_HTTPResponce_over_NC_limit2048(self):
        domains_status, err = namecheap_domains_check(
            domain_list=50*domains)
        self.assertEquals(domains_status, {'google.com': False,
                          'availabledomain.com': False,
                          u'раббота.com': True,
                          u'труд.com': False, 'alabaladomain.com': True})

    def test_get_HTTPResponce_no_domain_list(self):
        domains_status, err = namecheap_domains_check()
        self.assertEquals(domains_status, {})

    def test_get_HTTPResponce_dummy_domain_list(self):
        domains_status, err = namecheap_domains_check(['dummy'])
        self.assertEquals(domains_status, {})

    def test_parse(self):
        kw_sv_data = """ look	11

         when	13
        your	14
        website	15

        similar	12
        ttt  34
        ttqt  asd
        """
        kw_sv_dict = parser_data(kw_sv_data)
        self.assertDictEqual(kw_sv_dict,
                             {'look': '11', 'similar': '12',
                              'ttqt': 'asd', 'ttt': '34',
                              'website': '15', 'when': '13', 'your': '14'})


if __name__ == '__main__':
    unittest.main()
