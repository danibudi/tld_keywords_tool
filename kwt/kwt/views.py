from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.template.context import RequestContext
from models import Keyword, Tld, Kw_sv_language, Language
from forms import LanguageForm, KwdSvForm, KeywordListForm, KeywordDbForm
from namecheap_api import namecheap_domains_check, parser_data
from django.forms.formsets import formset_factory


def tld_flag(k, tld_all, namecheap_domains, uid):
    for tld in tld_all:
        url = k + '.' + tld
        kw = namecheap_domains.get(url)
        yield tld, kw, uid.next()


def kw_sort(language=None, method=None):
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


@csrf_exempt
def home(request):
    kw_language = None
    language = None
    kw_sv_dict = None
    form_errors = []
    form_kwd_sv = KwdSvForm(prefix='kw_sv_sub')
    if request.method == 'POST':
        form_kwd_sv = KwdSvForm(request.POST, prefix='kw_sv_sub')
        if 'kw_sv_sub' in request.POST:
            if form_kwd_sv.is_valid():
                kw_sv_data = form_kwd_sv.cleaned_data['kwd_sv']
                kw_sv_dict = parser_data(kw_sv_data)
                for k, v in kw_sv_dict.items():
                    try:
                        kw, created = Keyword.objects.get_or_create(
                            kw_english=str(k).lower())
                        kw.sv_english = int(v)
                        kw.save()
                    except:
                        pass
        if form_kwd_sv.is_valid():
            try:
                language = Language.objects.get(request.session["name"])
            except:
                language = form_kwd_sv.cleaned_data['language']
            else:
                language = None
            #~ request.session["name"] = language.id
            kwords_untranslated = kw_sort(language=language)
            KeywordListFormSet = formset_factory(KeywordListForm, extra=0)
            if ('lang_sub' in request.POST or 'kw_sv_sub' in request.POST) and language is not None:
                x_post = [
                    dict(kw_english=kw,
                         language=language.id) for kw in kwords_untranslated]
                formset = KeywordListFormSet(initial=x_post, prefix='trans_kw')
            else:
                formset = KeywordListFormSet(data=request.POST,
                                             prefix='trans_kw')
            if 'clear_trans_kw' in request.POST:
                if language:
                    language=language.id
                else:
                    language=None
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
        'st.html',
        dict(language=language, kw_sv_dict=kw_sv_dict, form_errors=form_errors,
             kw_language=kw_language, form_kwd_sv=form_kwd_sv,
             formset=formset, kwords_all=kwords_untranslated),
        context_instance=RequestContext(request))


@csrf_exempt
def grid(request):
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
            except:
                kw_language = None
            tld_all = [d.strip() for d in domains.split(',')]
            for kw in kw_language:
                kw_domain_list.append([kw.kw + '.' + t for t in tld_all])
                kw_sv.append((kw.kw, kw.sv))
            kw = [kw.kw for kw in kw_language]
            kw_domain_list = sum(kw_domain_list, [])
            namecheap_domains, err = namecheap_domains_check(kw_domain_list)
            grid_id = iter(xrange(10000))
            grid = []
            for k in kw_sv:
                t = tld_flag(k[0], tld_all, namecheap_domains, grid_id)
                grid.append((k[0], k[1], tuple(t)))
            return render_to_response(
                'grid.html', dict(domains=domains,
                                  namecheap_domains=namecheap_domains,
                                  form_lang=form_lang,
                                  tld_all=tld_all, kw=kw, grid=grid,
                                  context_instance=RequestContext(request)))
    else:
        form_lang = LanguageForm(prefix='pfix')
    return render_to_response(
        'grid.html', dict(
            domains=None, namecheap_domains=namecheap_domains,
            form_lang=form_lang,
            context_instance=RequestContext(request)))


@csrf_exempt
def kw_db(request):
    kw = Keyword.objects.all().order_by('kw_english')
    form = KeywordDbForm(request.POST)
    return render_to_response(
        'kw_db.html', dict(
            form=form, kw=kw,
            context_instance=RequestContext(request)))


@csrf_exempt
def kw_db1(request, kw_english):
    current_kw = Keyword.objects.get(id=kw_english)
    tr_kw = Kw_sv_language.objects.all().filter(kw_english=current_kw)
    return render_to_response(
        'kw_db1.html', dict(
            current_kw=current_kw, tr_kw=tr_kw,
            context_instance=RequestContext(request)))
