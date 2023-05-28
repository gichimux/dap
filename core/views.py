from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate 
from django.contrib import messages
from posts.models import *
from posts.forms import *
from django.contrib.auth.forms import AuthenticationForm 
from accounts.models import Profile 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.forms import EditProfileForm


def home(request):
    
    my_profile = Profile.objects.get(user=request.user)
    posts = Post.objects.all()
    
    if request.method == 'POST':
        product_form = NewProductForm(request.POST)
        swap_form = NewSwapForm(request.POST)

        if product_form.is_valid():
            product_form.instance.posted_by = request.user
            product_form.save()
            messages.success(request, 'Your product has been posted')
            return redirect(request.META['HTTP_REFERER'])
        
        if swap_form.is_valid():
            swap_form.instance.posted_by = request.user
            swap_form.save()
            messages.success(request, 'Your product has been posted')
            return redirect(request.META['HTTP_REFERER'])
        
    else:
        product_form = NewProductForm(request.POST)
        swap_form = NewSwapForm(request.POST)

    context ={
     'product_form': product_form,
     'posts' : posts,
     'swap_form': swap_form,
     'my_profile': my_profile,
   }
    return render (request, 'app/home.html', context )

@login_required
def user_profile(request):
    my_profile = Profile.objects.get(user=request.user)
    edit_profile_form = EditProfileForm(request.POST, instance=my_profile)

    if edit_profile_form.is_valid():
            edit_profile_form.save()
            messages.success(request, 'Your profile has been updated successfully')
            return redirect(request.META['HTTP_REFERER'])
    else:
        edit_profile_form = EditProfileForm(instance=my_profile)

    context ={
     'my_profile': my_profile,
     'edit_profile_form': edit_profile_form,
   }
    return render (request, 'profiles/userprofile.html', context )


@login_required
def post_detail(request, id):
    

    post_detail = Post.objects.get(id=id)
    post_comments = Comment.objects.filter(related_post=post_detail)
    
    if request.method == 'POST':
        post_comment_form = NewCommentForm(request.New)
    
        if post_comment_form.is_valid():
            post_comment_form.instance.comment_by = request.user
            post_comment_form.instance.related_post = post_detail
            post_comment_form.save()
            messages.success(request, 'Your profile has been updated successfully')
            return redirect(request.META['HTTP_REFERER'])
    else:
        new_comment_form = NewCommentForm(request.POST)


    context ={
     'post_detail': post_detail,
     'post_comments':post_comments,
     'new_comment_form': new_comment_form,

   }
    return render (request, 'posts/postdetail.html', context )

@login_required
def free_store(request):
       
    context ={
     
   }
    return render (request, 'markets/freestore.html', context )

@login_required
def baraza(request):
       
    context ={
     
   }
    return render (request, 'posts/baraza.html', context )


@login_required
def chat_list(request):
       
    context ={
     
   }
    return render (request, 'chats/chatlist.html', context )

def explore(request):
       
    context ={
     
   }
    return render (request, 'search/explore.html', context )


@login_required
def notification_list(request):
       
    context ={
     
   }
    return render (request, 'notifications/notificationlist.html', context )

@login_required
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


def delete_post(request, id):
    query = Post.objects.get(id=id)
    query.delete()
    return redirect('home')
