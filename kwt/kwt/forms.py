from django.forms import ModelForm, Form
from models import Keyword, Tld, Kw_sv_language, Language
from django import forms
from django.forms.formsets import BaseFormSet, formset_factory



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

class Kw_sv_languageForm(Form):
    #~ language = forms.ModelChoiceField(lang_all, required=True)
    kw = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'disabled', 'readonly': 'readonly'}))
    sv = forms.DecimalField(widget=forms.TextInput(
        attrs={'class': 'disabled', 'readonly': 'readonly'}))



class KwdSvForm(Form):
    kwd_sv = forms.CharField(widget=forms.Textarea, required=False,
                             max_length=200, help_text='200 characters max.')
    language = forms.ModelChoiceField(lang_all, required=False)


class KeywordListForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(KeywordListForm, self).__init__(*args, **kwargs)
        self.fields['sv'].widget.attrs = {'style': 'width:20%;'}
        self.fields['kw'].widget.attrs = {'style': 'width:auto;'}
        self.fields['kw_english'].widget.attrs = {'style': 'width:10%;'}
        self.fields['language'].widget.attrs = {'style': 'width:0%;'}
        self.fields['language'].widget.attrs = {'style': 'display: none;'}
        self.fields['language'].label=''
        self.fields['kw_english'].label=''
        self.fields['kw'].label=''
        self.fields['sv'].label=''

    class Meta:
        model = Kw_sv_language
        widgets = dict(
            kw_english=forms.TextInput(attrs={'class': 'disabled', 'readonly': 'readonly', 'style': 'width:100px;'}),
            kw=forms.TextInput(attrs={'style': 'width:100px;'}),
        )


class KeywordTldForm(Form):
    kw = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'disabled', 'readonly': 'readonly'}))
    sv = forms.DecimalField(widget=forms.TextInput(
        attrs={'class': 'disabled', 'readonly': 'readonly'}))
    domains = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                        choices=OPTIONS)


class KeywordLangForm(Form):
    kw = forms.CharField(widget=forms.TextInput(
        attrs={}))
    sv = forms.DecimalField(widget=forms.TextInput(
        attrs={}))
    kw_english_id = forms.DecimalField(widget=forms.TextInput(
        attrs={'class': 'disabled', 'readonly': 'readonly'}))

#~ FORM

class BaseUploadFormSet(BaseFormSet):

    def __init__(self, **kwargs):
        self.language = kwargs['language']
        del kwargs['language']
        super(BaseUploadFormSet, self).__init__(**kwargs)


    def _construct_form(self, i, **kwargs):
        kwargs["language"] = self.language
        return super(BaseUploadFormSet, self)._construct_form(i, **kwargs)


class UploadForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.language = kwargs['language']
        del kwargs['language']
        super(UploadForm, self).__init__(*args, **kwargs)
    engl_id = forms.DecimalField(widget=forms.TextInput(
        attrs={'class': 'disabled', 'readonly': 'readonly'}))
    kw = forms.CharField(widget=forms.TextInput(
        attrs={}))
    sv = forms.DecimalField(widget=forms.TextInput(
        attrs={}))
