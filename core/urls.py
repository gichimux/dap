from django.urls import  path
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [ 
    path("home/", views.home, name="home"),
    path("home/view_post", views.view_post, name="view_post"),

    path("home/post_detail/<int:id>", views.post_detail, name="post_detail"),
    path("chats/", views.chat_list, name="chat_list"),
    path("delete_post/<int:id>", views.delete_post, name="delete_post"),

    path("home/baraza", views.baraza, name="baraza"),
    path("explore/", views.explore, name="explore"),
    path("home/my_tokens", views.my_tokens, name="my_tokens"),

    path('post/<int:post_id>/upvote/', views.upvote_post, name='upvote_post'),
    path('post/<int:post_id>/downvote/', views.downvote_post, name='downvote_post'),
    path('posts/<int:post_id>/get_comment_count/', views.get_comment_count, name='get_comment_count'),

    # url(r'^ajax/uploads/$', views.uploadData, name='uploadData'),
    path('posts/<int:post_id>/add_comment/', views.add_comment, name='add-comment'),

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
    path('posts/<int:post_id>/toggle_bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
    # path("profile/", views.profile, name="profile"),
    path('posts/<int:post_id>/toggle_repost/', views.toggle_repost, name='toggle_repost'),

    # topics filter
    path('topics/general/', views.topic_filter, {'topic': 'general'}, name='topic_general'), 
    path('topics/science_technology/', views.topic_filter, {'topic': 'science_technology'}, name='topic_science & technology'),
    path('topics/faith_religion/', views.topic_filter, {'topic': 'faith & religion'}, name='topic_faith & religion'),
    path('topics/business/', views.topic_filter, {'topic': 'business & finance'}, name='topic_business & finance'),
    path('topics/art/', views.topic_filter, {'topic': 'art'}, name='topic_art'),
    path('topics/culture/', views.topic_filter, {'topic': 'culture'}, name='topic_culture'),
    path('topics/sports/', views.topic_filter, {'topic': 'sports'}, name='topic_sports'),
    path('topics/news/', views.topic_filter, {'topic': 'news'}, name='topic_news'),
    path('topics/music/', views.topic_filter, {'topic': 'music'}, name='topic_music'),
    path('topics/history/', views.topic_filter, {'topic': 'history'}, name='topic_history'),
    path('topics/philosophy/', views.topic_filter, {'topic': 'philosophy'}, name='topic_philosophy'),
    path('topics/fiction/', views.topic_filter, {'topic': 'fiction'}, name='topic_fiction'),
    path('topics/health_wellness/', views.topic_filter, {'topic': 'health & wellness'}, name='topic_health & wellness'),
    path('topics/design/', views.topic_filter, {'topic': 'design'}, name='topic_design'),
    path('topics/education/', views.topic_filter, {'topic': 'education'}, name='topic_education'),
    path('topics/humor/', views.topic_filter, {'topic': 'humor'}, name='topic_humor'),
    path('topics/literature/', views.topic_filter, {'topic': 'literature'}, name='topic_literature'),
    path('topics/politics/', views.topic_filter, {'topic': 'politics'}, name='topic_politics'),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)