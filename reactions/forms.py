from django import forms


class NewCommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    parent = forms.CharField(required=False)
