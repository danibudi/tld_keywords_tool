from django.db import models


class Keyword(models.Model):
    kw_english = models.CharField("keyword in English", unique=True, max_length=200)
    sv_english = models.PositiveIntegerField('search volume in English', default=0)

    def __unicode__(self):
        return  u'%s' % (self.kw_english)

    def clean(self):
        self.kw_english = self.kw_english.lower()


class Tld(models.Model):
    domain = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return  u'%s' % (self.domain)

    def clean(self):
        self.domain = self.domain.lower()


class Language(models.Model):
    language = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
            return  u'%s' % (self.language)


class Kw_sv_language(models.Model):
    kw_english = models.ForeignKey(Keyword, verbose_name="keyword in English")
    language = models.ForeignKey(Language)
    kw = models.CharField("keyword", max_length=200)
    sv = models.PositiveIntegerField('search volume', default=1)

    def __unicode__(self):
        return  u'%s' % (self.kw)

    def clean(self):
        self.kw = self.kw.lower()
        self.kw = self.kw.strip().split(' ')[0]

    class Meta:
        unique_together = ("language", "kw")
