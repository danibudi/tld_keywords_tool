from django.shortcuts import render_to_response, render
from django.views.decorators.csrf import csrf_exempt
from django.template.context import RequestContext
from models import Keyword, Tld, Kw_sv_language
from forms import LanguageForm, KwdSvForm, KeywordListForm
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
        k_trans = Kw_sv_language.objects.filter(kw_english=k, language=language)
        if k_trans.count() == 0:
            kw_non_translated.append(k)
    print 25, kw_non_translated, language
    return kw_non_translated


@csrf_exempt
def home(request):
    kw_language = None
    language = None
    kw_sv_dict = None
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
                            kw_english=str(k))
                        kw.sv_english = int(v)
                        kw.save()
                    except:
                        print k, v
        if form_kwd_sv.is_valid():
            language = form_kwd_sv.cleaned_data['language']
            kwords_untranslated = kw_sort(language=language)
            KeywordListFormSet = formset_factory(KeywordListForm, extra=0)
            if 'lang_sub' in request.POST or 'kw_sv_sub' in request.POST and language is not None:
                x_post = [dict(kw_english=kw, language=language.id) for kw in kwords_untranslated]
                formset = KeywordListFormSet(initial=x_post, prefix='trans_kw')
            else:
                formset = KeywordListFormSet(data=request.POST, prefix='trans_kw')
                #~ for form_tr in formset:
                    #~ form_tr.lan
    if language is None:
        kwords_untranslated = Keyword.objects.all()
        KeywordListFormSet = formset_factory(KeywordListForm, extra=0)
        x_post = [dict(kw_english=kw) for kw in kwords_untranslated]
        formset = KeywordListFormSet(initial=x_post, prefix='trans_kw')
    if request.GET.get('sort') == "id" or not 'sort' in request.GET:
        kwords_all = kw_sort(language=language)
    if request.GET.get('sort') == "alphabetic":
        kwords_all = kw_sort(language=language, method='kw_english')
    if request.GET.get('sort') == 'descend':
        kwords_all = kw_sort(language=language, method='sv_english')
    #~ return render_to_response(
    return render(request,
        'st.html',
        dict(language=language, kw_sv_dict=kw_sv_dict,
             kw_language=kw_language,  # formset_len=formset_len,
             form_kwd_sv=form_kwd_sv,
             formset=formset,
             kwords_all=kwords_untranslated, context_instance=RequestContext(request)))


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
