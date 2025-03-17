from django import forms

class CreateCommentForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={'class':"form-control tm-color-secondary col-12"}
        )
    )