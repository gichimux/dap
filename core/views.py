from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate 
from posts.models import *
from posts.forms import *
from chats.models import *
from notifications.models import *

from random import sample
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm 
from accounts.models import User, Profile 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.forms import *
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
    nat_c = Post.objects.filter(topic="nature").count()   
    spo_c = Post.objects.filter(topic="sports").count()   
    bus_c = Post.objects.filter(topic="business & finance").count()   
    new_c = Post.objects.filter(topic="news").count()   
    mus_c = Post.objects.filter(topic="music").count()   
    his_c = Post.objects.filter(topic="history").count()
    phi_c = Post.objects.filter(topic="philosophy").count()   
    hea_c = Post.objects.filter(topic="health & wellness").count()   
    art_c = Post.objects.filter(topic="art & design").count()   

    posts = Post.objects.all()
    res = {'success': True, 'message': 'Your post has posted'}

    current_user = request.user
    following_users = current_user.profile.followers.all()
    # Get users the current user is not following (excluding themselves)
    not_following_users = User.objects.exclude(id=current_user.id).exclude(id__in=following_users)

    # Randomly select two users to display
    random_users = sample(list(not_following_users), 2)


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
        'nat_c': nat_c,
        'sci_c': sci_c,
        'bus_c': bus_c,
        'art_c': art_c,
        'new_c': new_c,
        'cul_c': cul_c,
        'spo_c': spo_c,
        'mus_c': mus_c,
        'his_c': his_c,
        'phi_c': phi_c,
        'rel_c': rel_c,
        'hea_c': hea_c,
        'random_users': random_users,
        'post_form': post_form,
        'posts': posts,
        'my_profile': my_profile,
    }
    return render(request, 'app/home.html', context)

@login_required
def upload_post(request):
    if request.method == 'POST':
        # Assuming you have a form with fields 'topic', 'body', and 'post_image'

        # Get form data from the request
        topic = request.POST.get('topic')
        body = request.POST.get('body')
        post_image = request.FILES.get('post_image')

        # Check if required data is provided
        if topic and body:
            # Create a new Post instance
            new_post = Post(
                topic=topic,
                body=body,
                post_image=post_image,  # This is the image field in your Post model
                posted_by=request.user  # Assuming you're using Django's built-in User model
            )
            new_post.save()

            response_data = {'success': True, 'message': 'Post submitted successfully.'}
            return JsonResponse(response_data)
        else:
            response_data = {'success': False, 'message': 'Invalid form data.'}
            return JsonResponse(response_data)

    # Handle GET or other HTTP methods
    response_data = {'success': False, 'message': 'Invalid request method.'}
    return JsonResponse(response_data)


def upload_avatar(request):
    if request.method == 'POST' and request.FILES['avatar']:
        avatar = request.FILES['avatar']
        request.user.profile.avatar = avatar
        request.user.profile.save()
        return JsonResponse({'avatar_url': request.user.profile.avatar.url})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@require_POST
def update_profile(request):
    if request.method == 'POST':
        # Handle the uploaded cover image
        if 'cover_image' in request.FILES:
            cover_image = request.FILES['cover_image']
            request.user.profile.cover_image = cover_image

        # Handle the uploaded avatar image
        if 'avatar' in request.FILES:
            avatar = request.FILES['avatar']
            request.user.profile.avatar = avatar

        # Update other profile information
        request.user.profile.name = request.POST.get('name', '')
        request.user.profile.location = request.POST.get('location', '')
        request.user.profile.website = request.POST.get('website', '')
        request.user.profile.bio = request.POST.get('bio', '')

        # Save the updated profile
        request.user.profile.save()

        return JsonResponse({'message': 'Profile updated successfully.'})

    return JsonResponse({'error': 'Invalid request method.'}, status=400)
 
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
def follow_user(request):
    if request.method == 'POST':
        username_to_follow = request.POST.get('username')
        try:
            user_to_follow = User.objects.get(username=username_to_follow)
            request.user.profile.following.add(user_to_follow)
            return JsonResponse({'success': True})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@login_required
def who_to_follow(request):
    current_user = request.user
    following_users = current_user.profile.followers.all()
    # Get users the current user is not following (excluding themselves)
    not_following_users = User.objects.exclude(id=current_user.id).exclude(id__in=following_users)

    # Randomly select two users to display
    random_users = sample(list(not_following_users), 2)

    context = {
        'random_users': random_users,
    }

    return render(request, 'who_to_follow.html', context)
 
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

        # Create an alert for the post owner
        if post.posted_by != request.user:
            Alert.objects.create(
                sender=request.user,
                receiver=post.posted_by,
                alert_type='like',
                post=post,
            )

        return JsonResponse({'success': True, 'vote_count': post.vote_count})
    return JsonResponse({'success': False})

def upvote_comment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    if request.user.is_authenticated:
        comment.upvote(request.user)

        # Create an alert for the comment owner
        if comment.comment_by != request.user:
            Alert.objects.create(
                sender=request.user,
                receiver=comment.comment_by,
                alert_type='like',
                comment=comment,
            )

        return JsonResponse({'success': True, 'vote_count': comment.vote_count})
    return JsonResponse({'success': False})

def upvote_reply(request, reply_id):
    reply = Reply.objects.get(pk=reply_id)
    if request.user.is_authenticated:
        reply.upvote(request.user)

        # Create an alert for the reply owner
        if reply.reply_by != request.user:
            Alert.objects.create(
                sender=request.user,
                receiver=reply.reply_by,
                alert_type='like',
                reply=reply,
            )

        return JsonResponse({'success': True, 'vote_count': reply.vote_count})
    return JsonResponse({'success': False})



# @login_required
# def private_chat_view(request, other_user_id):
#     other_user = get_object_or_404(User, id=other_user_id)
#     # Create or retrieve a chat room between the current user and the other user
#     chat_room, created = ChatRoom.objects.get_or_create(user1=request.user, user2=other_user)
#     return render(request, 'private_chat_room.html', {'chat_room': chat_room})


def downvote_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.user.is_authenticated:
        post.downvote(request.user)
        return JsonResponse({'success': True, 'vote_count': post.vote_count})
    return JsonResponse({'success': False})
  

def downvote_comment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    if request.user.is_authenticated:
        comment.downvote(request.user)
        return JsonResponse({'success': True, 'vote_count': comment.vote_count})
    return JsonResponse({'success': False})
  

def downvote_reply(request, reply_id):
    reply = Reply.objects.get(pk=reply_id)
    if request.user.is_authenticated:
        reply.downvote(request.user)
        return JsonResponse({'success': True, 'vote_count': reply.vote_count})
    return JsonResponse({'success': False})
  

def toggle_follow(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    profile_to_follow = user_to_follow.profile
    user_profile = request.user.profile

    if user_profile != profile_to_follow:
        if user_profile.following.filter(id=profile_to_follow.id).exists():
            user_profile.following.remove(profile_to_follow)
            followed = False
        else:
            user_profile.following.add(profile_to_follow)
            followed = True

        return JsonResponse({'followed': followed})
    else:
        return JsonResponse({'error': 'You cannot follow yourself'})
       
   
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
    profile_user = get_object_or_404(User, username=profile_username)
    profile_detail = Profile.objects.get(user=profile_user)
    profile_posts = Post.objects.filter(posted_by=profile_user)
    posts_count = profile_posts.count()
    profile = request.user.profile

    # Check if the logged-in user follows the profile_user
    follows = request.user.profile.following.filter(user=profile_user).exists()

    # Check if the profile_user follows the logged-in user
    followed_by = profile_user.profile.following.filter(user=request.user).exists()

    if request.method == 'POST':
        edit_profile_form = EditProfileForm(request.POST, request.FILES, instance=profile)

        if edit_profile_form.is_valid():
            edit_profile_form.save()
            messages.success(request, 'Your profile has been updated successfully')
            return redirect(request.META['HTTP_REFERER'])
    else:
        edit_profile_form = EditProfileForm(instance=profile)

        messages.error(request, 'Profile update failed. Please check the form.')

    context = {
        'profile_user': profile_user,
        'profile_detail': profile_detail,
        'profile_posts': profile_posts,
        'posts_count': posts_count,
        'edit_profile_form': edit_profile_form,
        'follows': follows,  # Pass the follows information to the template
        'followed_by': followed_by,  # Pass the followed_by information to the template
    }
    
    return render(request, 'profiles/userprofile.html', context)

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

        # Create an alert for the post owner
        if post.posted_by != request.user:
            Alert.objects.create(
                sender=request.user,
                receiver=post.posted_by,
                alert_type='comment',
                post=post,
            )

        return JsonResponse({'message': 'Comment added successfully'})
    else:
        return JsonResponse({'error': 'Comment text is required'}, status=400)
    
@require_POST
def add_reply(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    reply_text = request.POST.get('reply')

    if reply_text:
        reply = Reply.objects.create(
            reply_by=request.user,
            parent_comment=comment,
            body=reply_text
        )
        comment.reply_count += 1
        comment.save()

        # Create an alert for the post owner
        if comment.comment_by != request.user:
            Alert.objects.create(
                sender=request.user,
                receiver=comment.comment_by,
                alert_type='reply',
                comment=comment,
            )

        return JsonResponse({'message': 'reply added successfully'})
    else:
        return JsonResponse({'error': 'reply text is required'}, status=400)
    
       
def get_comment_count(request, post_id):
    post = Post.objects.get(id=post_id)
    comment_count = Comment.objects.filter(parent_post=post).count()
    return JsonResponse({'comment_count': comment_count})

def get_reply_count(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    reply_count = Reply.objects.filter(related_comment=comment).count()
    return JsonResponse({'reply_count': reply_count})

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
def shop(request):
       
    context ={
     
   }
    return render (request, 'markets/shop.html', context )

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

@login_required
def edit_profile(request):

        # Retrieve the current user's profile
    profile = request.user.profile

    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():

            form.save()
            profile_url = reverse('view_profile', args=[request.user.username])

            return redirect(profile_url)  # Redirect to the edit profile page after a successful update
    else:
        # Create a form instance and populate it with the current profile data
        form = EditProfileForm(instance=profile)

    context = {
        'form': form,
    }
       

    return render (request, 'profiles/edit_profile.html', context )


@login_required
def view_alerts(request):
    # Retrieve unread alerts for the logged-in user
    user_alerts = Alert.objects.filter(receiver=request.user, is_read=False)

    # Mark retrieved alerts as read
    user_alerts.update(is_read=True)

    context = {'user_alerts': user_alerts}
    return render(request, 'notifications/notificationlist.html', context)


def landing(request):
		
    form = LoginForm(request, data=request.POST)
    signup_form = NewUserForm(request.POST)
    if request.method == "POST":
        if signup_form.is_valid():
            user = signup_form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect(edit_profile)
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
    form = LoginForm()
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
