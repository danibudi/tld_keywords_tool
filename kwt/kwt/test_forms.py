from django.test import TestCase
import unittest
from django.test.client import Client

from models import Kw_sv_language, Language, Keyword  #, , Tld,


class Kw_sv_languageTestCase(TestCase):
    def setUp(self):
        self.language, self.created_l = Language.objects.get_or_create(pk=2)
        self.kw_english, self.created_kw = Keyword.objects.get_or_create(kw_english='bonus', sv_english=1111)

    def test_home(self):
        client = Client()
        response = client.get('/home/')
        self.assertEqual(response.status_code, 200)

    def test_root(self):
        client = Client()
        response = client.get('')
        self.assertEqual(response.status_code, 200)

    def test_kw_created(self):
        "KW IS CREATED"
        Kw_sv_language.objects.create(language=self.language, kw_english=self.kw_english, kw="spanish_2", sv=111)
        kw = Kw_sv_language.objects.get(kw="spanish_2")
        self.assertGreaterEqual(kw.id, 1)

    def test_empty_kw_not_created(self):
        "empty kw is not CREATED"
        try:
            Kw_sv_language.objects.create(language=self.language, kw_english=self.kw_english, kw="", sv=111)
        except Exception as i:
            print Exception, dir(Exception)
            self.assertEqual("""'IntegrityError', "columns language_id, kw are not unique""", i.message)

    def test_kw_not_propper_sv_not_created(self):
        "KW with not propper sv is not CREATED"
        try:
            Kw_sv_language.objects.create(language=self.language, kw_english=self.kw_english, kw="", sv='dummy')
        except Exception as i:
            self.assertEqual("""invalid literal for int() with base 10: 'dummy'""", i.args[0])

    def test_kw_negative_sv_not_created(self):
        "KW with not propper sv is not CREATED"
        try:
            Kw_sv_language.objects.get_or_create(language=self.language, kw_english=self.kw_english, kw="dummy_kw", sv='-169')
        except Exception as i:
            print i, dir(i)
            self.assertEqual("""columns language_id, kw are not unique""", i.args[0])
        #~ self.assertGreaterEqual(Kw_sv_language.objects.get(kw="dummy_kw", sv='-69'), 1)
        print  [a.sv for a in Kw_sv_language.objects.all()]
        self.assertGreaterEqual(Kw_sv_language.objects.get(kw="dummy_kw", sv='-169').sv, 0)

    def test_no_language(self):
        "language is not selected"
        try:
            Kw_sv_language.objects.create(language=None, kw_english=self.kw_english, kw="dummy_kw", sv='69')
            self.assertIsNone(Kw_sv_language.objects.get(kw="dummy_kw", sv='69'))
        except Exception as i:
            self.assertEqual("""Cannot assign None: "Kw_sv_language.language" does not allow null values.""", i.args[0])


if __name__ == '__main__':
    unittest.main(
        #~ defaultTest="Kw_sv_languageTestCase.test_kw_negative_sv_not_created"
        )