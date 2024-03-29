from ast import Mod
from dataclasses import field
from django import forms
from .models import *
from django.forms import ModelForm, TextInput, Textarea

class PostForm(forms.ModelForm):
    category= forms.ChoiceField(choices=Topics.choices, label="Topic")

    class Meta:
        model = Post
        fields = ( 'topic', 'body')


class NewCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )


class NewReplyForm(ModelForm):
    class Meta:
        model = Reply
        fields = ('body', )


class BookmarkForm(forms.Form):
    post_id = forms.IntegerField()