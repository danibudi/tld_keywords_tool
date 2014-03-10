from django.contrib import admin
from models import Keyword, Language, Kw_sv_language, Tld


class Kw_sv_languageAdmin(admin.ModelAdmin):
    list_display = ('kw_english', 'language', 'kw', 'sv')
    fieldsets = [
        (None,               {'fields': ['kw_english']}),
        ('Language information', {'fields': ['language', 'kw', 'sv']}),
    ]
    list_filter = ['language', 'sv']


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('id', 'language')
    list_filter = ['language']

class TldAdmin(admin.ModelAdmin):
    list_display = ('id', 'domain')

class Kw_sv_languageInline(admin.StackedInline):
    model = Kw_sv_language
    model._meta.verbose_name_plural = "Keywords in other languages"
    model._meta.verbose_name = "Keyword"
    extra = 3

class KeywordAdmin(admin.ModelAdmin):
    list_display = ('kw_english', 'sv_english')
    list_filter = ['sv_english']
    inlines = [Kw_sv_languageInline]


admin.site.register(Kw_sv_language, Kw_sv_languageAdmin)
admin.site.register(Tld, TldAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Keyword, KeywordAdmin)