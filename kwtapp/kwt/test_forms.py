from django.test import TestCase
import unittest
from django.test.client import Client

from models import Kw_sv_language, Language, Keyword
from forms import KeywordListForm


class Kw_sv_languageTestCase(TestCase):
    def setUp(self):
        self.language = Language.objects.create(pk=2)
        self.kw_english = Keyword.objects.create(
            kw_english='bonus', sv_english=1111)

    def test_home(self):
        client = Client()
        response = client.get('/home/')
        self.assertEqual(response.status_code, 200)

    def test_root(self):
        client = Client()
        response = client.get('')
        self.assertEqual(response.status_code, 200)

    def test_kw_created(self):
        "KW is CREATED"
        ## Instantiate form
        form = KeywordListForm(data={'sv': 42,
                                     'kw': 'bonus-tr',
                                     'kw_english': self.kw_english.id,
                                     'language': self.language.id})
        ## call is_valid() to create cleaned_data
        self.assertTrue(form.is_valid())

    def test_empty_kw_not_created(self):
        "empty kw is not CREATED"
        ## Instantiate form
        form = KeywordListForm(data={'sv': -169,
                                     'kw': '',
                                     'kw_english': self.kw_english.id,
                                     'language': self.language.id})
        ## call is_valid() to create cleaned_data
        self.assertFalse(form.is_valid())
        self.assertIn('kw', form.errors)

    def test_kw_not_propper_sv_not_created(self):
        "KW with not propper sv is not CREATED"
        form = KeywordListForm(data={'sv': 'dummy',
                                     'kw': '',
                                     'kw_english': self.kw_english.id,
                                     'language': self.language.id})
        ## call is_valid() to create cleaned_data
        self.assertFalse(form.is_valid())
        self.assertIn('sv', form.errors)
        self.assertIn('kw', form.errors)

    def test_kw_negative_sv_not_created(self):
        "KW with negative sv is not CREATED"
        ## Instantiate form
        form = KeywordListForm(data={'sv': -169,
                                     'kw': 'alabala',
                                     'kw_english': self.kw_english.id,
                                     'language': self.language.id})
        ## call is_valid() to create cleaned_data
        self.assertFalse(form.is_valid())
        self.assertIn('sv', form.errors)

    def test_no_language(self):
        "language is not selected"
        form = KeywordListForm(data={'sv': -169,
                                     'kw': 'alabala',
                                     'kw_english': self.kw_english.id,
                                     'language': None})
        ## call is_valid() to create cleaned_data
        self.assertFalse(form.is_valid())
        self.assertIn('language', form.errors)


if __name__ == '__main__':
    unittest.main()
