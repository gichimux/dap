from ast import Mod
from dataclasses import field
from django import forms
from .models import *
from django.forms import ModelForm

class NewSellForm(ModelForm):
    class Meta:
        model = Post
        fields = ('about', 'display_price', 'price_limit', 'product_condition', 'product_pick_up', 'payment_method'  )


# class NewPostForm(ModelForm):
#     class Meta:
#         model = Product
#         fields = ('product_name', 'condition', 'description', 'category', 'tags' )



# class NewCategoryForm(ModelForm):
#     class Meta:
#         model = Category
#         fields = ( 'category_name','category_image')

