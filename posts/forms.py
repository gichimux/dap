from ast import Mod
from dataclasses import field
from django import forms
from .models import *
from django.forms import ModelForm

class NewProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ( 'post_location', 'product_condition', 'about', 'display_price', 'product_pick_up', 'payment_method')

class NewSwapForm(ModelForm):
    class Meta:
        model = Swap
        fields = ( 'post_location', 'about', 'swap_pick_up', 'swap_condition')


class NewCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('comment', )


class NewReplyForm(ModelForm):
    class Meta:
        model = Reply
        fields = ('comment', )

