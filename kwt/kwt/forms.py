from django.forms import ModelForm, Form
from models import Tld, Kw_sv_language, Language
from django import forms


tlds = Tld.objects.all()
t_list = [t.domain for t in tlds]
t_list = ", ".join(t_list)
lang_all = Language.objects.all()
tlds = Tld.objects.all()
OPTIONS = tuple([(t.id, t.domain) for t in tlds])


class LanguageForm(Form):
    language = forms.ModelChoiceField(lang_all, required=True)
    tld_list = forms.CharField(max_length=None, required=True, label='TLD',
                               initial=t_list, help_text='80 characters max.')


class KwdSvForm(Form):
    kwd_sv = forms.CharField(widget=forms.Textarea, required=False,
                             max_length=200, help_text='200 characters max.')
    language = forms.ModelChoiceField(
        lang_all.order_by('language'),
        widget=forms.Select(
            attrs={"onChange": 'click_submit()'}), required=False)

    def __init__(self, *args, **kwargs):
        super(KwdSvForm, self).__init__(*args, **kwargs)
        self.fields['kwd_sv'].label = "Keywords&SV"


class KeywordListForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(KeywordListForm, self).__init__(*args, **kwargs)
        self.fields['sv'].widget.attrs = {'style': 'width:99%'}
        self.fields['kw'].widget.attrs = {'style': "width:30%"}
        self.fields['kw'].widget.attrs = {'placeholder': 'translated keyword'}
        self.fields['kw_english'].widget.attrs = {
            'style': 'width:99%; readonly: readonly; \
            background-color: rgba(246, 235, 235, 1)'}
        self.fields['language'].widget.attrs = {'style': 'width:0%;'}
        self.fields['language'].widget.attrs = {'style': 'display: none;'}
        self.fields['language'].label = ''
        self.fields['kw_english'].label = ''
        self.fields['kw'].label = ''
        self.fields['sv'].label = ''

    class Meta:
        model = Kw_sv_language
        widgets = dict(
            kw_english=forms.TextInput(
                attrs={"class": "disabled"}),
        )


class KeywordDbForm(Form):
    kw = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'disabled', 'readonly': 'readonly'}))
    sv = forms.DecimalField(widget=forms.TextInput(
        attrs={'class': 'disabled', 'readonly': 'readonly'}))
    language = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'disabled', 'readonly': 'readonly'}))
    kw_translated = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'disabled', 'readonly': 'readonly'}))
    sv_translated = forms.DecimalField(widget=forms.TextInput(
        attrs={'class': 'disabled', 'readonly': 'readonly'}))


class KeywordTldForm(Form):
    kw = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'disabled', 'readonly': 'readonly'}))
    sv = forms.DecimalField(widget=forms.TextInput(
        attrs={'class': 'disabled', 'readonly': 'readonly'}))
    domains = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                        choices=OPTIONS)


class KeywordLangForm(Form):
    kw = forms.CharField(widget=forms.TextInput(attrs={}))
    sv = forms.DecimalField(widget=forms.TextInput(attrs={}))
    kw_english_id = forms.DecimalField(widget=forms.TextInput(
        attrs={'class': 'disabled', 'readonly': 'readonly'}))
