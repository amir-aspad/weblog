from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget


class CreateCommentForm(forms.Form):
    text = forms.CharField(
        widget=CKEditor5Widget(
            attrs={'class':"form-control tm-color-secondary col-12 django_ckeditor_5", 'rows':10},
            config_name='simple'
        )
    )