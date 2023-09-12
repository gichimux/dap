from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile
from django.forms import ModelForm, TextInput, EmailInput, PasswordInput, IntegerField, SelectDateWidget, URLInput, Textarea
from datetime import datetime
User = get_user_model()

# Create your forms here.

class NewUserForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'validate', 'placeholder': 'Username'}),
        label=False
    )
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'validate', 'placeholder': 'Your Email'}),
        label=False
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'validate', 'placeholder': 'Password'}),
        label=False
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'validate', 'placeholder': 'Confirm Password'}),
        label=False
    )
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        
    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username','password']
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
        self.fields['username'].label = False
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password'}) 
        self.fields['password'].label = False
        
class EditProfileForm(ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'profile-edit', 'placeholder': 'Your Name'}),
        label=False
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'profile-edit', 'placeholder': 'Phone Number'}),
        label=False
    )
    birthday = forms.DateField(widget=SelectDateWidget(years=range(1900, datetime.now().year + 1)))
    website = forms.CharField(
        widget=forms.URLInput(attrs={'class': 'profile-edit', 'placeholder': 'Your Website Link'}),
        label=False
    )
    location = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'profile-edit', 'placeholder': 'Location'}),
        label=False
    )
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'profile-textarea', 'placeholder': 'Your Bio'}),
        label=False
    )
    class Meta:
        model = Profile
        fields = ('name',  'phone_number', 'birthday', 'website', 'location', 'bio')
    
    # def __init__(self, *args, **kwargs):
    #     super(EditProfileForm, self).__init__(*args, **kwargs)
    #     instance = getattr(self, 'instance', None)
    #     if instance and instance.pk:
    #         self.fields['birth_date'].initial = instance.birthday


# class ProfileForm(ModelForm):
#     class Meta:
#         model = Profile
#         fields = ('first_name', 'last_name', 'phone_number', 'avatar')
        