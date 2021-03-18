from django import forms
from s3direct.widgets import S3DirectWidget

from accounts.models import Profile

class ProfileForm(forms.ModelForm):
    # profile_picture = forms.ImageField(required=False, \
    #  error_messages ={'invalid':("Image files only")},\
    #  widget=forms.FileInput)
    profile_picture = forms.URLField(widget=S3DirectWidget(dest='example_destination'))

    class Meta:
        model = Profile
        fields = ['profile_picture','website', 'country', 'location', 'display_email', 'bio', 'youtube_link', 'facebook_link', 'instagram_link', 'linkedin_link',]
        widgets = {
			'bio': forms.Textarea(attrs={'rows': 3}),
		}