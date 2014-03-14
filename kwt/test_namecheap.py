#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from namecheap_api import namecheap_domains_check, parser_data

domains = [u'alabaladomain.com', u'раббота.com', u'труд.com',
           u'availabledomain.com', u'google.com']


class TestApi(unittest.TestCase):
    def test_get_HTTPResponce(self):
        domains_status, err = namecheap_domains_check(domain_list=domains)
        self.assertEquals(domains_status,
                          {'google.com': False,  # 'vintech.com': 'false',
                           'availabledomain.com': False, u'раббота.com': True,
                           u'труд.com': True, 'alabaladomain.com': True})
        domains_status, err = namecheap_domains_check()
        self.assertEquals(domains_status, {})
        domains_status, err = namecheap_domains_check('dummy')
        self.assertEquals(domains_status, {})

    def test_parse(self):
        kw_sv_data = """ look	11

         when	13
        your	14
        website	15

        similar	12
        """
        kw_sv_list = parser_data(kw_sv_data)
        self.assertEqual(kw_sv_list, [
            ['look', '11'], ['when', '13'], ['your', '14'],
            ['website', '15'], ['similar', '12']])


if __name__ == '__main__':
    unittest.main(defaultTest='TestApi.test_parse')
