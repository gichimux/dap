from ast import Mod
from dataclasses import field
from django import forms
from .models import *
from django.forms import ModelForm

class NewSellForm(ModelForm):
    class Meta:
        model = Post
        fields = ( 'post_location', 'product_condition', 'about', 'sale_price',  'product_pick_up', 'payment_method')

class NewSwapForm(ModelForm):
    class Meta:
        model = Post
        fields = ( 'post_location', 'product_condition', 'about', 'gold_price', 'product_pick_up', 'payment_method')


class NewCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('comment', )


class NewReplyForm(ModelForm):
    class Meta:
        model = Reply
        fields = ('comment', )

