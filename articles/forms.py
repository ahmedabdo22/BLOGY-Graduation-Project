from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            "title", "category", "tags", "content", "cover_image",
            "status", "seo_title", "seo_description","publication"
        ]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 10}),
            "tags": forms.CheckboxSelectMultiple(),
        }
