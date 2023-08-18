from django.urls import  path
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [ 
    path("home/", views.home, name="home"),
    path("home/view_post", views.view_post, name="view_post"),

    path("home/post_detail/<int:id>", views.post_detail, name="post_detail"),
    path("home/chats/", views.chat_list, name="chat_list"),
    path("delete_post/<int:id>", views.delete_post, name="delete_post"),

    path("home/baraza", views.baraza, name="baraza"),
    path("home/explore", views.explore, name="explore"),
    path("home/my_tokens", views.my_tokens, name="my_tokens"),

    path('post/<int:post_id>/upvote/', views.upvote_post, name='upvote_post'),
    path('post/<int:post_id>/downvote/', views.downvote_post, name='downvote_post'),

    url(r'^ajax/uploads/$', views.uploadData, name='uploadData'),

    path("", views.landing, name="landing"),
    path("@<str:profile_username>", views.view_profile, name="view_profile"),
    
    path('follow/<str:profile_username>/', views.follow_user, name='follow_user'),
    path('unfollow/<str:profile_username>/', views.unfollow_user, name='unfollow_user'),
    # path("follow/@<str:profile_username>/",views.follow_toggle, name="follow_toggle"),
    path("@<str:profile_username>/following", views.follow_list, name="follow_list"),
    # path("like/<int:post_id>/",views.like_toggle, name="like_toggle"),
    path("search/", views.post_search, name="search_results"),

    # path("free_store/", views.free_store, name="free_store"),
    path("notification_list/", views.notification_list, name="notification_list"),
    path("settings/", views.settings_list, name="settings_list"),

    path("bookmark_list/", views.bookmark_list, name="bookmark_list"),
    path('api/bookmark-toggle/', views.bookmark_toggle, name='bookmark-toggle'),
    # path("profile/", views.profile, name="profile"),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)