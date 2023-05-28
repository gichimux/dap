from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.forms import ModelForm

User = get_user_model()

# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user


class EditProfileForm(ModelForm):
    
    class Meta:
        model = Profile
        fields = ('name', 'location', 'bio')

# class ProfileForm(ModelForm):
#     class Meta:
#         model = Profile
#         fields = ('first_name', 'last_name', 'phone_number', 'avatar')
        