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
from django.views.decorators.http import require_POST

def home(request):
    # if request.user.is_authenticated:
    my_profile = Profile.objects.get(user=request.user)
    # my_profile = "" 
    
    #filters
    gen_c = Post.objects.filter(topic="general").count()
    sci_c = Post.objects.filter(topic="science & technology").count()   
    cul_c = Post.objects.filter(topic="culture").count()   
    rel_c = Post.objects.filter(topic="faith & religion").count()   
    pol_c = Post.objects.filter(topic="politics").count()   
    spo_c = Post.objects.filter(topic="sports").count()   
    bus_c = Post.objects.filter(topic="business & finance").count()   
    new_c = Post.objects.filter(topic="news").count()   
    mus_c = Post.objects.filter(topic="music").count()   
    his_c = Post.objects.filter(topic="history").count()
    phi_c = Post.objects.filter(topic="philosophy").count()   
    fic_c = Post.objects.filter(topic="fiction").count()   
    hea_c = Post.objects.filter(topic="health & wellness").count()   
    art_c = Post.objects.filter(topic="art").count()   
    des_c = Post.objects.filter(topic="design").count()   
    edu_c = Post.objects.filter(topic="education").count()   
    hum_c = Post.objects.filter(topic="humor").count()   
    lit_c = Post.objects.filter(topic="literature").count()   

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
        'gen_c': gen_c,
        'pol_c': pol_c,
        'sci_c': sci_c,
        'bus_c': bus_c,
        'art_c': art_c,
        'new_c': new_c,
        'cul_c': cul_c,
        'spo_c': spo_c,
        'mus_c': mus_c,
        'his_c': his_c,
        'phi_c': phi_c,
        'fic_c': fic_c,
        'rel_c': rel_c,
        'hea_c': hea_c,
        'des_c': des_c,
        'edu_c': edu_c,
        'hum_c': hum_c,
        'lit_c': lit_c,
        'post_form': post_form,
        'posts': posts,
        'my_profile': my_profile,
    }
    return render(request, 'app/home.html', context)


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
    

def toggle_bookmark(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user in post.bookmarked_users.all():
        post.bookmarked_users.remove(request.user)
    else:
        post.bookmarked_users.add(request.user)

    return JsonResponse({'success': True})

@login_required
def bookmark_list(request):
    bookmarked_posts = request.user.bookmarked_posts.all()
    context = {
        'bookmarked_posts': bookmarked_posts,
    }
    return render(request, 'posts/bookmark_list.html', context)

@login_required
def toggle_repost(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    try:
        repost = Repost.objects.get(post=post, reposted_by=request.user)
        repost.delete()
        is_reposted = False
    except Repost.DoesNotExist:
        Repost.objects.create(post=post, reposted_by=request.user)
        is_reposted = True

    return JsonResponse({'success': True, 'is_reposted': is_reposted})
   
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


@require_POST
def add_comment(request, post_id):
    post = Post.objects.get(id=post_id)
    comment_text = request.POST.get('comment')

    if comment_text:
        comment = Comment.objects.create(
            comment_by=request.user,
            parent_post=post,
            body=comment_text
        )
        post.comment_count += 1
        post.save()

        return JsonResponse({'message': 'Comment added successfully'})
    else:
        
        return JsonResponse({'error': 'Comment text is required'}, status=400)

def get_comment_count(request, post_id):
    post = Post.objects.get(id=post_id)
    comment_count = Comment.objects.filter(parent_post=post).count()
    return JsonResponse({'comment_count': comment_count})

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

def topic_filter(request, topic):
    filtered_posts = Post.objects.filter(topic=topic)
    context ={
        'filtered_posts': filtered_posts,
        'topic': topic
        }
    return render(request, 'topics/topic_posts.html', context)


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
