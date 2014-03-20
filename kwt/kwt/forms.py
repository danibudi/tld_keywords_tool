from django.forms import ModelForm, Form
from models import Keyword, Tld, Kw_sv_language, Language
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


class LanguagesAllForm(Form):
    language = forms.ModelChoiceField(lang_all, required=True)


class KwdSvForm(Form):
    kwd_sv = forms.CharField(widget=forms.Textarea, required=True,
                             max_length=200, help_text='200 characters max.')


class KeywordListForm(ModelForm):
    kw_english = forms.ModelMultipleChoiceField(queryset=Keyword.objects.all())
    sv_kw_english = forms.DecimalField(required=False)

    def __init__(self, *args, **kwargs):
        super(KeywordListForm, self).__init__(*args, **kwargs)
        self.fields['kw_english'].widget.attrs = {'style': 'width:175px;'}
        self.fields['sv_kw_english'].widget.attrs = {'style': 'width:175px;'}

    def clean_kw_english(self):
        kw_english = self.cleaned_data.get('kw_english')
        sv_kw_english = Keyword.objects.get(kw_english=kw_english)
        sv_kw_english = sv_kw_english.sv_english

    class Meta:
        model = Kw_sv_language


class KeywordTldForm(Form):
    kw = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'disabled', 'readonly': 'readonly'}))
    sv = forms.DecimalField(widget=forms.TextInput(
        attrs={'class': 'disabled', 'readonly': 'readonly'}))
    domains = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                        choices=OPTIONS)
