from django import forms
from django.contrib.auth.models import User
from pages.models import Documents, Profile


class SignUpForm(forms.ModelForm):
    password = forms.CharField(max_length=32, widget=forms.PasswordInput(), label="Password")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password',)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('user_type',)


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Documents
        fields = ('title', 'image', 'pdf', 'description',)
