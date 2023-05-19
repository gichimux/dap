from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate 
from django.contrib import messages
from posts.models import Post,Post_Type
from posts.forms import NewSellForm
from django.contrib.auth.forms import AuthenticationForm 
# from accounts.models import Profile 
from django.contrib import messages

def home(request):
    
    posts = Post.objects.all()
    
    if request.method == 'POST':
        sell_form = NewSellForm(request.POST)

        if sell_form.is_valid():
            sell_form.instance.posted_by = request.user
            sell_form.instance.post_type = Post_Type.SELL
            sell_form.save()
            messages.success(request, 'Your product has been posted')
            return redirect(request.META['HTTP_REFERER'])
    else:
        sell_form = NewSellForm(request.POST)

    context ={
     'sell_form': sell_form,
   }
    return render (request, 'app/home.html', context )

def user_profile(request):
       
    context ={
     
   }
    return render (request, 'profiles/userprofile.html', context )

def free_store(request):
       
    context ={
     
   }
    return render (request, 'markets/freestore.html', context )

def chat_list(request):
       
    context ={
     
   }
    return render (request, 'chats/chatlist.html', context )

def notification_list(request):
       
    context ={
     
   }
    return render (request, 'notifications/notificationlist.html', context )

def settings_list(request):
       
    context ={
     
   }
    return render (request, 'settings/settingslist.html', context )




def landing(request):
		
    form = AuthenticationForm(request, data=request.POST)

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Welcome, you are now logged in as {username}.")
                return redirect("home")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    context ={
        "login_form": form,
    }
    return render (request, 'core/index.html', context )