from django.db import models


class Keyword(models.Model):
    kw_english = models.CharField("keyword in English", unique=True, max_length=200)
    sv_english = models.IntegerField('search volume in English', default=0)

    def __unicode__(self):
        return  u'%s' % (self.kw_english)


class Tld(models.Model):
    domain = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return  u'%s' % (self.domain)


class Language(models.Model):
    language = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
            return  u'%s' % (self.language)


class Kw_sv_language(models.Model):
    kw_english = models.ForeignKey(Keyword, verbose_name="keyword in English")
    language = models.ForeignKey(Language)
    kw = models.CharField("keyword", max_length=200)
    sv = models.IntegerField('search volume', default=0)

    def __unicode__(self):
        return  u'%s' % (self.kw)
