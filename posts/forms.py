from django import forms

from .models import Post, Category

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'tags','content','featured_image','category','language','membership',]