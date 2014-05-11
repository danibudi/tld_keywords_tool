from django.db import models
from django.core.exceptions import ValidationError


def validate_sv(value):
    #validators - ensure positive in sqlite3
    if value <= 0:
        raise ValidationError('%s is not a positive number' % value)


def validate_kw(value):
    #~ validator for kw without spaces
    value = value.lower()
    value = value.strip().split(' ')[0]


class Keyword(models.Model):
    "model for english kw"
    kw_english = models.CharField("keyword in English", unique=True,
                                  max_length=200, validators=[validate_kw])
    sv_english = models.PositiveIntegerField('search volume in English',
                                             default=0,
                                             validators=[validate_sv])

    def __unicode__(self):
        return u'%s' % (self.kw_english)


class Tld(models.Model):
    "model for top level domains"
    domain = models.CharField(max_length=200, unique=True,
                              validators=[validate_kw])

    def __unicode__(self):
        return u'%s' % (self.domain)


class Language(models.Model):
    "model for language"
    language = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return u'%s' % (self.language)


class Kw_sv_language(models.Model):
    "model for non-english kw - unique (language, kw)"
    kw_english = models.ForeignKey(Keyword, verbose_name="keyword in English")
    language = models.ForeignKey(Language)
    kw = models.CharField("keyword", max_length=200, validators=[validate_kw])
    sv = models.PositiveIntegerField('search volume', default=1,
                                     validators=[validate_sv])

    def __unicode__(self):
        return u'%s' % (self.kw)

    class Meta:
        unique_together = ("language", "kw")
