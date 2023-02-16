from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = ['author', 'author_name', 'category', 'title', 'text', 'rating']

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("title")
        text = cleaned_data.get("text")

        if name == text:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data