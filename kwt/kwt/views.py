from django.shortcuts import render_to_response, redirect
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.template.context import Context, RequestContext
from django.contrib.auth.models import Group, User
from django.shortcuts import render
from django.http import HttpResponseRedirect
import settings
from models import Keyword, Tld, Language, Kw_sv_language
from forms import KeywordForm, KeywordListForm, KeywordTldForm, LanguageForm
from django.forms.formsets import formset_factory
from namecheap_api import namecheap_domains_check
import unittest


def tld_flag(k, tld_all, namecheap_domains, uid):
        for t in tld_all:
            url = k+'.'+t
            b = namecheap_domains.get(url)
            yield t, b, uid.next()


@csrf_exempt
def home(request):
    user = request.user
    domains = []
    form = KeywordForm()
    #~ KeywordFormSet = formset_factory(KeywordForm, max_num=4, extra=2)

    if form.is_valid():
        kw_english = form.cleaned_data['kw_english']
        sv_english = form.cleaned_data['sv_english']
        form.save()
    if request.GET.get('sort') == "id" or not request.GET.has_key('sort'):
        kwords_all = Keyword.objects.all()
    if request.GET.get('sort') == "alphabetic":
        kwords_all = Keyword.objects.order_by('kw_english')
    if request.GET.get('sort') == 'descend':
        kwords_all = Keyword.objects.order_by('sv_english')
    return render_to_response(
        'st.html',
        dict(static_url=settings.STATIC_URL, media=settings.MEDIA_ROOT,
             form=form,#, form_kwl=form_kwl,
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
