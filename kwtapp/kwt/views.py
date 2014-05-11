"""An app for using Namecheap.com, requires registration in Namecheap.com.
    can be partially tested for free with sandbox.
    Username, key and pass are in local_settings.py

.. author:: Dani Budinova <d.budinova@gmail.com>

"""
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.template.context import RequestContext
from models import Keyword, Tld, Kw_sv_language, Language
from forms import (LanguageForm, KwdSvForm, KeywordListForm,
                   KeywordDbForm, TranslatedForm)
from namecheap_api import namecheap_domains_check, parser_data, parser_data_to_list
from django.forms.formsets import formset_factory


def tld_flag(kwd, tld_all, namecheap_domains, uid):
    """prepare data for grid with kws and tlds
    tld_all - list
    kwd - (kw.kw, kw.sv)
    namecheap_domains_check(domain_list=[]):
    the exact limit of the amount of the domains that
    can be checked in one API call is 120
    there's a limitation on the string length for GET -
    the length of a URL is limited to 2048 characters maximum.
    https://community.namecheap.com/forums/viewtopic.php?f=17&t=7568"""
    for tld in tld_all:
        url = kwd + '.' + tld
        kw = namecheap_domains.get(url)
        yield tld, kw, uid.next()


def kw_sort(language=None, method=None):
    """This function sort Keyword-objects.
    Args:
       language (kwt.models.Language):  The language to use.
       method (str):  alphabetically
    Returns:
       list with  non_translated Keywords"""
    kw_non_translated = []
    if method:
        kwords_all = Keyword.objects.order_by(method)
    else:
        kwords_all = Keyword.objects.all()
    for k in kwords_all:
        k_trans = Kw_sv_language.objects.filter(kw_english=k,
                                                language=language)
        if k_trans.count() == 0:
            kw_non_translated.append(k)
    return kw_non_translated


def add_english_kwds(form_kwd_sv):
    """add or update the english kwds written in textarea KwdSvForm"""
    if form_kwd_sv.is_valid():
        kw_sv_data = form_kwd_sv.cleaned_data['kwd_sv']
        kw_sv_dict = parser_data(kw_sv_data)
        for k, v in kw_sv_dict.items():
            try:
                kw, created = Keyword.objects.get_or_create(
                    kw_english=str(k).lower())
                kw.sv_english = int(v)
                kw.save()
            except Exception:
                pass
    return


@csrf_exempt
def home(request):
    """function for kw_add.html, add english words from textarea - KwdSvForm
    and translated words from a table - formset with KeywordListForm"""
    kw_language = None
    language = None
    kw_sv_dict = None
    form_errors = []
    form_kwd_sv = KwdSvForm(prefix='kw_sv_sub')
    if request.method == 'POST':
        form_kwd_sv = KwdSvForm(request.POST, prefix='kw_sv_sub')
        if 'kw_sv_sub' in request.POST:
            add_english_kwds(form_kwd_sv=form_kwd_sv)
        if form_kwd_sv.is_valid():
            try:
                language = Language.objects.get(request.session["name"])
            except Exception:
                language = form_kwd_sv.cleaned_data['language']
            else:
                language = None
            kwords_untranslated = kw_sort(language=language)
            KeywordListFormSet = formset_factory(KeywordListForm, extra=0)
            if ('lang_sub' in request.POST or 'kw_sv_sub' in request.POST)\
                    and language is not None:
                x_post = [
                    dict(kw_english=kw,
                         language=language.id) for kw in kwords_untranslated]
                formset = KeywordListFormSet(initial=x_post, prefix='trans_kw')
            else:
                formset = KeywordListFormSet(data=request.POST,
                                             prefix='trans_kw')
            if 'clear_trans_kw' in request.POST:
                if language:
                    language = language.id
                else:
                    language = None
                x_post = [dict(
                    kw_english=kw,
                    language=language) for kw in kwords_untranslated]
                formset = KeywordListFormSet(initial=x_post, prefix='trans_kw')
            if 'trans_kw' in request.POST:
                for form_kw_lang in formset:
                    if form_kw_lang.is_valid():
                        form_kw_lang.save()
                    else:
                        form_errors.append(form_kw_lang.errors)
                c = {'kw': [u'This field is required.']}
                for i in range(len(form_errors)):
                    if c in form_errors:
                        form_errors.remove(c)
                #~ form can accept atleast 1 kw, no error messages for empty kws
                kwords_untranslated = kw_sort(language=language)
                if language:
                    x_post = [dict(
                        kw_english=kw,
                        language=language.id) for kw in kwords_untranslated]
                    request.session["name"] = language.id
                else:
                    x_post = []
                formset = KeywordListFormSet(initial=x_post, prefix='trans_kw')
    if language is None:
        kwords_untranslated = Keyword.objects.all()
        KeywordListFormSet = formset_factory(KeywordListForm, extra=0)
        x_post = [dict(kw_english=kw) for kw in kwords_untranslated]
        formset = KeywordListFormSet(initial=x_post, prefix='trans_kw')
    return render_to_response(
        'kw_add.html',
        dict(language=language, form_errors=form_errors,
             kw_language=kw_language, form_kwd_sv=form_kwd_sv,
             formset=formset, kwords_all=kwords_untranslated),
        context_instance=RequestContext(request))


@csrf_exempt
def manykw(request):
    """function for manykw.html, add english words from textarea - KwdSvForm
    and translated words from textarea - TranslatedForm"""
    kw_language = None
    language = None
    kw_sv_list = None
    form_errors = []
    kwords_untranslated = []
    new_kwds_list_errors = []
    form_kwd_sv = KwdSvForm(prefix='kw_sv_sub')
    form_tr_kwd_sv = TranslatedForm(prefix='tr_kw_sv_sub')
    if request.method == 'POST':
        form_kwd_sv = KwdSvForm(request.POST, prefix='kw_sv_sub')
        form_tr_kwd_sv = TranslatedForm(request.POST, prefix='tr_kw_sv_sub')
        if 'kw_sv_sub' in request.POST:
            add_english_kwds(form_kwd_sv)
        if form_kwd_sv.is_valid():
            try:
                language = Language.objects.get(request.session["name"])
            except Exception:
                language = form_kwd_sv.cleaned_data['language']
            else:
                language = None
            kwords_untranslated = kw_sort(language=language)
            if 'tr_kw_sv_sub' in request.POST:
                if form_tr_kwd_sv.is_valid():
                    kw_sv_data = form_tr_kwd_sv.cleaned_data['kwd_sv_tr']
                    #~ kw_sv_dict = parser_data(kw_sv_data)
                    kw_sv_list = parser_data_to_list(kw_sv_data)
                    new_kwds_list = zip([
                        i.id for i in kwords_untranslated], kw_sv_list)
                    if not new_kwds_list:
                        new_kwds_list_errors.append('kw & sv needed')
                    for eng_kw_id, transl_kw in new_kwds_list:
                        try:
                            kw = Kw_sv_language.objects.create(
                                kw_english=Keyword.objects.get(
                                    id=int(eng_kw_id)),
                                kw=str(transl_kw[0]).lower().strip(),
                                sv=int(transl_kw[1]),
                                language=language
                                )
                        except Exception as why:
                            # __str__ allows args to printed directly
                            new_kwds_list_errors.append(
                                [why, (eng_kw_id, transl_kw)])
                    kwords_untranslated = kw_sort(language=language)
                else:
                    form_tr_kwd_sv.append(form_tr_kwd_sv.errors)
    if language is None:
        kwords_untranslated = Keyword.objects.all()
        form_kwd_sv = KwdSvForm(prefix='kw_sv_sub')
    return render_to_response(
        'manykw.html',
        dict(language=language, form_errors=form_errors,
             kw_language=kw_language, form_kwd_sv=form_kwd_sv,
             form_tr_kwd_sv=form_tr_kwd_sv,
             new_kwds_list_errors=new_kwds_list_errors,
             kwords_all=kwords_untranslated),
        context_instance=RequestContext(request))


@csrf_exempt
def grid(request):
    """view for lookup free domains"""
    tlds = Tld.objects.all()
    t_list = [t.domain for t in tlds]
    t_list = ", ".join(t_list)
    kw_domain_list = []
    kw_sv = []
    namecheap_domains = None
    err = None
    form_lang = LanguageForm(request.POST, prefix='pfix')
    if request.method == 'POST':
        if form_lang.is_valid():
            language = form_lang.cleaned_data['language']
            domains = form_lang.cleaned_data['tld_list']
            try:
                kw_language = Kw_sv_language.objects.filter(language=language)
            except Exception:
                kw_language = None
            tld_all = [d.strip() for d in domains.split(',')]
            for kw in kw_language:
                kw_domain_list.append([kw.kw + '.' + t for t in tld_all])
                kw_sv.append((kw.kw, kw.sv))
            kw = [kw.kw for kw in kw_language]
            kw_domain_list = sum(kw_domain_list, [])
            try:
                namecheap_domains, err = namecheap_domains_check(
                    kw_domain_list)
            except Exception:
                return render_to_response(
                    'grid.html', dict(
                        domains=None, namecheap_domains=namecheap_domains,
                        form_lang=form_lang,
                        exception_error="""
                        <urlopen error [Errno-2] Name or service not known>""",
                        context_instance=RequestContext(request)))
            grid_id = iter(xrange(10000))
            grid = []
            for kw in kw_sv:
                tld_flags = tld_flag(kw[0], tld_all,
                                     namecheap_domains, grid_id)
                grid.append((kw[0], kw[1], tuple(tld_flags)))
            return render_to_response(
                'grid.html', dict(domains=domains,
                                  namecheap_domains=namecheap_domains,
                                  form_lang=form_lang,
                                  tld_all=tld_all, kw=kw, grid=sorted(grid),
                                  context_instance=RequestContext(request)))
    else:
        form_lang = LanguageForm(prefix='pfix')
    return render_to_response(
        'grid.html', dict(
            domains=None, namecheap_domains=namecheap_domains,
            form_lang=form_lang,
            context_instance=RequestContext(request)))


def kw_db(request):
    "view KW datebase"
    kw = Keyword.objects.all().order_by('kw_english')
    form = KeywordDbForm(request.POST)
    return render_to_response(
        'kw_db.html', dict(
            form=form, kw=kw,
            context_instance=RequestContext(request)))


def kw_db1(request, kw_english):
    "show translations&sv for the selected kw as: 'French: chat 15'"
    current_kw = Keyword.objects.get(id=kw_english)
    tr_kw = Kw_sv_language.objects.all().filter(kw_english=current_kw)
    return render_to_response(
        'kw_db1.html', dict(
            current_kw=current_kw, tr_kw=tr_kw,
            context_instance=RequestContext(request)))
