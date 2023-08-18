from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate 
from posts.models import *
from posts.forms import *
from django.contrib.auth.forms import AuthenticationForm 
from accounts.models import User, Profile 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.forms import EditProfileForm
from django.shortcuts import get_object_or_404 
import json
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from accounts.forms import NewUserForm
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt

def home(request):
    my_profile = Profile.objects.get(user=request.user)
    posts = Post.objects.all()
    res = {'success': True, 'message': 'Your post has posted'}

    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)  # Include request.FILES here
        if post_form.is_valid():
            try:
                # Attempt to get the logged-in user's profile
                my_profile = Profile.objects.get(user=request.user)
            except ObjectDoesNotExist:
                pass  # Handle this case if necessary
            
            post = post_form.save(commit=False)  # Don't commit the post yet
            post.posted_by = request.user
            post.save()
            
            return JsonResponse(res)
        else:
            res = {'success': False, 'message': 'Form data is invalid.'}
            return JsonResponse(res)
    else:
        post_form = PostForm()

    context = {
        'post_form': post_form,
        'posts': posts,
        'my_profile': my_profile,
    }
    return render(request, 'app/home.html', context)


def uploadData(request):
    res = {'error': True, 'msg': "Something went wrong."}
    allowed_files = ["jpg", "jpeg", "png"]
    posted_by = request.user
    if request.method == "POST" :
        headline = request.POST['headline']
        body = request.POST['body']
        post_image = request.FILES['post_image']

        ErrorF = {'error': False, "msg": ""}
        if headline and body  and post_image:
             
            if not ErrorF['error']:
                u = Post.objects.create(posted_by=posted_by, headline=headline, body=body, post_image=post_image)
                u.save()
                res = {'error': False, 'msg': "Successfully Submited."}
            elif ErrorF['error']:
                res = ErrorF
            else:
                res = {'error': True, 'msg': "Form not submitted. Try with a refresh."}
        else:
            res = {'error': True, 'msg': "Fill all required fields."}
        return JsonResponse(res)

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
def follow_user(request, profile_username):
    if request.is_ajax():
        profile_user = Profile.objects.get(user__username=profile_username)
        current_user_profile = request.user.profile

        if current_user_profile not in profile_user.followers.all():
            profile_user.followers.add(current_user_profile)
            response_data = {'success': True, 'action': 'follow'}
        else:
            response_data = {'success': False, 'message': 'You are already following this user.'}

        return JsonResponse(response_data)

@login_required
def unfollow_user(request, profile_username):
    if request.is_ajax():
        profile_user = Profile.objects.get(user__username=profile_username)
        current_user_profile = request.user.profile

        if current_user_profile in profile_user.followers.all():
            profile_user.followers.remove(current_user_profile)
            response_data = {'success': True, 'action': 'unfollow'}
        else:
            response_data = {'success': False, 'message': 'You are not following this user.'}

        return JsonResponse(response_data)
    
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

@csrf_exempt
def bookmark_toggle(request):
    if request.method == 'POST':
        user = request.user
        post_id = request.POST.get('post_id')
        
        post = get_object_or_404(Post, id=post_id)
        
        try:
            bookmark = Bookmark.objects.get(user=user, post=post)
            bookmark.delete()
            message = 'Bookmark removed successfully'
        except Bookmark.DoesNotExist:
            bookmark = Bookmark.objects.create(user=user, post=post)
            message = 'Bookmark added successfully'

        return JsonResponse({'message': message}, status=200)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def bookmark_list (request):
    my_profile = Profile.objects.get(user=request.user)

    user = request.user
    bookmarked_posts = Bookmark.objects.filter(user=user)
    context ={
     'bookmarked_posts': bookmarked_posts,
     'my_profile': my_profile,
    }
    
    return render (request, 'posts/bookmark_list.html', context )

    
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
    
def upvote_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.user.is_authenticated:
        post.upvote(request.user)
        return JsonResponse({'success': True, 'vote_count': post.vote_count})
    return JsonResponse({'success': False})

def downvote_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.user.is_authenticated:
        post.downvote(request.user)
        return JsonResponse({'success': True, 'vote_count': post.vote_count})
    return JsonResponse({'success': False})
  

   
   
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
    post_comments = Comment.objects.filter(parent_post=post_detail)
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
def view_post(request):
    
    post_detail = Post.objects.filter(posted_by=request.user).last()
   
    context ={
     'post_detail': post_detail,
     
   }
    return render (request, 'posts/view_post.html', context )


@login_required
def my_tokens(request):
       
    context ={
     
   }
    return render (request, 'tokens/my_tokens.html', context )
 
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
    signup_form = NewUserForm(request.POST)
    if request.method == "POST":
        if signup_form.is_valid():
            user = signup_form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect(view_profile)
        messages.error(request, "Unsuccessful registration. Invalid information.")

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
    signup_form = NewUserForm()
    context ={
        "login_form": form,
        "signup_form": signup_form,
    }
    return render (request, 'core/index.html', context )


def delete_post(request, id):
    query = Post.objects.get(id=id)
    query.delete()
    return redirect('home')
