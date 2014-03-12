from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.template.context import RequestContext
from models import Keyword, Tld, Kw_sv_language
from forms import KeywordForm, LanguageForm, LanguagesAllForm
from django.forms.formsets import formset_factory
from namecheap_api import namecheap_domains_check


def tld_flag(k, tld_all, namecheap_domains, uid):
    for tld in tld_all:
        url = k + '.' + tld
        kw = namecheap_domains.get(url)
        yield tld, kw, uid.next()


@csrf_exempt
def home(request):
    kw_language = None
    language = None
    kwords_all = Keyword.objects.all()
    form = KeywordForm(request.POST)
    KeywordFormSet = formset_factory(KeywordForm)
    if request.method == 'POST':
        if 'nc_sub' in request.POST:
            formset = KeywordFormSet(request.POST)
            if formset.is_valid():
                for form1 in formset:
                    form1.save()
        else:
            formset = KeywordFormSet()
        if 'lang_sub' in request.POST:
            form_lang = LanguagesAllForm(request.POST)
            if form_lang.is_valid():
                try:
                    language = form_lang.cleaned_data['language']
                    try:
                        kw_language = Kw_sv_language.objects.filter(
                            language=language)
                    except:
                        kw_language = None
                except:
                    language = ''
        else:
            form_lang = LanguagesAllForm()
    else:
        formset = KeywordFormSet()
        form_lang = LanguagesAllForm()

    if request.GET.get('sort') == "id" or not 'sort' in request.GET:
        kwords_all = kwords_all
    if request.GET.get('sort') == "alphabetic":
        kwords_all = Keyword.objects.order_by('kw_english')
    if request.GET.get('sort') == 'descend':
        kwords_all = Keyword.objects.order_by('sv_english')
    return render_to_response(
        'st.html',
        dict(formset=formset, language=language,
             form=form, form_lang=form_lang, kw_language=kw_language,
             kwords_all=kwords_all, context_instance=RequestContext(request)))


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
                                  form_lang=form_lang, formset=None,
                                  tld_all=tld_all, kw=kw, grid=grid,
                                  context_instance=RequestContext(request)))
    else:
        form_lang = LanguageForm(prefix='pfix')
    return render_to_response(
        'grid.html', dict(
            domains=None, namecheap_domains=namecheap_domains,
            form_lang=form_lang, formset=None,
            context_instance=RequestContext(request)))
