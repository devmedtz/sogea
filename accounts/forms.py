from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from allauth.account.forms import SignupForm

from .models import CustomUser,Profile


class CustomSignupForm(SignupForm):

    # Override the init method
    def __init__(self, *args, **kwargs):
        # Call the init of the parent class
        super().__init__(*args, **kwargs)


    # Put in custom signup logic
    def custom_signup(self, request, user):
        user_profile = Profile(user=user)
        user_profile.save()

        user.save()


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email',)
        

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        if len(password1) < 8:
            raise forms.ValidationError('Password too short, It must be 8 character or more')
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('email', 'password','is_active',)

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class SignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ['email', ]

class MyAuthForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _(
            "Email or Password is not correct"
        ),
        'inactive': _("This account is inactive."),
    }
