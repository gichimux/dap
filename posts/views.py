from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate 
from django.contrib import messages
from .models import *
from .forms import *


def post_detail(request, id):
    

    context ={
    #  'post': post
   }
    return render (request, 'posts/postdetail.html', context )

