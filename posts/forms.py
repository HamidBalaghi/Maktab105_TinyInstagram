from django import forms
from .models import Post, Image

from django import forms


class NewPostForm(forms.Form):
    description = forms.CharField(widget=forms.Textarea)
    image1 = forms.ImageField(required=True)
    image2 = forms.ImageField(required=False)
    image3 = forms.ImageField(required=False)
    image4 = forms.ImageField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        image1 = cleaned_data.get('image1')
        image2 = cleaned_data.get('image2')
        image3 = cleaned_data.get('image3')
        image4 = cleaned_data.get('image4')

        if not any([image1, image2, image3, image4]):
            raise forms.ValidationError("You must upload at least one image.")

        return cleaned_data
