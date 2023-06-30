from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate 
from django.contrib import messages
from posts.models import *
from posts.forms import *
from django.contrib.auth.forms import AuthenticationForm 
from accounts.models import User, Profile 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.forms import EditProfileForm
from django.shortcuts import get_object_or_404 
import json
from django.http import HttpResponse
from django.db.models import Q


def home(request):

    my_profile = Profile.objects.get(user=request.user)
    posts = Post.objects.all()
    
    if request.method == 'POST':
        sell_form = NewSellForm(request.POST)
        swap_form = NewSwapForm(request.POST)

        if sell_form.is_valid():
            sell_form.instance.posted_by = request.user
            sell_form.save()
            messages.success(request, 'Your post has been posted')
            return redirect(request.META['HTTP_REFERER'])

        if swap_form.is_valid():
            swap_form.instance.posted_by = request.user
            swap_form.save()
            messages.success(request, 'Your post has been posted')
            return redirect(request.META['HTTP_REFERER'])

    else:
        sell_form = NewSellForm(request.POST)
        swap_form = NewSwapForm(request.POST)

    context ={
     'sell_form': sell_form,
     'swap_form': swap_form,
     'posts' : posts,
     'my_profile': my_profile,
   }
    return render (request, 'app/home.html', context )

def post_search(request):
    if request.method == 'GET':
        query= request.GET.get('q')

        submitbutton= request.GET.get('submit')

        if query is not None:
            lookups= Q(about__icontains=query) | Q(post_location__icontains=query)

            results= Post.objects.filter(lookups).distinct()

            context={'results': results,
                     'submitbutton': submitbutton}

            return render(request, 'search/search.html', context)

        else:
            return render(request, 'search/search.html')

    else:
        return render(request, 'search/search.html')
    
@login_required
def follow_toggle(request, profile_username):
    user_id = User.objects.get(username=profile_username)
    profile_user = Profile.objects.get(user=user_id)
    
    authorObj = User.objects.get(id=user_id.id)
    currentUserObj = User.objects.get(id=request.user.id)
    following = profile_user.following.all()

    # if profile_username != currentUserObj.username:
    if currentUserObj.profile in following:
        profile_user.following.remove(currentUserObj.id)
    else:
        profile_user.following.add(currentUserObj.id)

    return redirect(request.META['HTTP_REFERER'])

@login_required
# def like_toggle(request, post_id):
#     post = Post.objects.get(id=post_id)
#     currentUserObj = User.objects.get(id=request.user.id)
    
#     likes = post.likes.all()

#     # if profile_username != currentUserObj.username:
#     if currentUserObj in likes:
#         post.likes.remove(currentUserObj.id)
#     else:
#         post.likes.add(currentUserObj.id)

#     return redirect(request.META['HTTP_REFERER'])

# def like_toggle(request, post_id):
#     if request.method == "POST":
#         post = Post.objects.get(id=post_id)
#         currentUserObj = User.objects.get(id=request.user.id)
#         likes = post.likes.all()
#         if currentUserObj in likes:
#             post.likes.remove(currentUserObj.id)
#             post.save() 
#             return render( request, 'posts/partials/likes_div.html', context={'post':post})
#         else:
#             post.likes.add(currentUserObj.id)
#             post.save() 
#             return render( request, 'posts/partials/likes_div.html', context={'post':post})
        
def customer_search(request):
    if request.method == 'GET':
        query= request.GET.get('q')

        submitbutton= request.GET.get('submit')

        if query is not None:
            lookups= Q(first_name__icontains=query) | Q(last_name__icontains=query)

            results= UnitTenant.objects.filter(lookups).distinct()

            context={'results': results,
                     'submitbutton': submitbutton}

            return render(request, 'search/customer_search.html', context)

        else:
            return render(request, 'search/customer_search.html')

    else:
        return render(request, 'search/customer_search.html')
    
def like_button(request):
   if request.method =="POST":
       if request.POST.get("operation") == "like_submit" and request.is_ajax():
         post_id=request.POST.get("post_id",None)
         post=get_object_or_404(Post,pk=post_id)
         if post.likes.filter(id=request.user.id): #already liked the post
            post.likes.remove(request.user) #remove user from likes 
            liked=False
         else:
             post.likes.add(request.user) 
             liked=True
         ctx={"likes_count":post.total_likes,"liked":liked,"post_id":post_id}
         return HttpResponse(json.dumps(ctx), content_type='application/json')
   
  

   
   
def follow_list(request, profile_username):
    user_id = User.objects.get(username=profile_username)
    profile_user = Profile.objects.get(user=user_id)
    # followers = Profile.objects.filter(fol)
    
    following = profile_user.following.all()
    followers = profile_user.followers.all()
    context ={
     'following': following,
     'followers': followers,
     'profile_user': profile_user,
     
    }
    
    return render (request, 'profiles/following_list.html', context )


def view_profile(request, profile_username):
    profile_user = User.objects.get(username=profile_username)
    profile_detail = Profile.objects.get(user=profile_user)
    profile_posts = Post.objects.filter(posted_by=profile_user)
    posts_count = profile_posts.count()

    edit_profile_form = EditProfileForm(request.POST, instance=profile_detail)

    if edit_profile_form.is_valid():
            edit_profile_form.save()
            messages.success(request, 'Your profile has been updated successfully')
            return redirect(request.META['HTTP_REFERER'])
    else:
        edit_profile_form = EditProfileForm(instance=profile_detail)

    context ={
     'posts_count': posts_count,
     'profile_posts': profile_posts,
     'profile_detail': profile_detail,
     'edit_profile_form': edit_profile_form,
    }
    
    return render (request, 'profiles/userprofile.html', context )



@login_required
def post_detail(request, id):
    
    post_detail = Post.objects.get(id=id)
    post_comments = Comment.objects.filter(related_post=post_detail)
    comment_counter = post_comments.count()
    if request.method == 'POST':
        post_comment_form = NewCommentForm(request.POST)
    
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
     'comment_counter':comment_counter,

   }
    return render (request, 'posts/post_detail.html', context )

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
    posts =  Post.objects.all() 
    context ={
     'posts': posts,
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
