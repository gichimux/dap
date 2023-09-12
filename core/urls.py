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
    path('upload_avatar/', views.upload_avatar, name='upload_avatar'),
    path('upload_images/', views.upload_images, name='upload_images'),

    # url(r'^ajax/uploads/$', views.uploadData, name='uploadData'),
    path('posts/<int:post_id>/add_comment/', views.add_comment, name='add-comment'),

    path("", views.landing, name="landing"),
    path("@<str:profile_username>", views.view_profile, name="view_profile"),
    path('edit_profile/', views.edit_profile, name='edit_profile'),

    path('toggle_follow/<str:username>/', views.toggle_follow, name='toggle_follow'),

    path('follow/<str:profile_username>/', views.follow_user, name='follow_user'),
    path('unfollow/<str:profile_username>/', views.unfollow_user, name='unfollow_user'),
    path('follow_user/', views.follow_user, name='follow_user'),
    # path("follow/@<str:profile_username>/",views.follow_toggle, name="follow_toggle"),
    path("@<str:profile_username>/following", views.follow_list, name="follow_list"),
    # path("like/<int:post_id>/",views.like_toggle, name="like_toggle"),
    path("search/", views.post_search, name="search_results"),
    path('private-chat/<int:other_user_id>/', views.private_chat_view, name='private_chat'),

    # path("free_store/", views.free_store, name="free_store"),
    path("notification_list/", views.notification_list, name="notification_list"),
    path("settings/", views.settings_list, name="settings_list"),

    path("bookmark_list/", views.bookmark_list, name="bookmark_list"),
    path('posts/<int:post_id>/toggle_bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
    # path("profile/", views.profile, name="profile"),
    path('posts/<int:post_id>/toggle_repost/', views.toggle_repost, name='toggle_repost'),

    # category filter
    path('category/cars/', views.category_filter, {'category': 'cars'}, name='category_cars'), 
    path('category/art/', views.category_filter, {'category': 'art'}, name='category_art'),
    path('category/motorbikes/', views.category_filter, {'category': 'motorbikes'}, name='category_motorbikes'),
    path('category/bicycles/', views.category_filter, {'category': 'bicycles'}, name='category_bicycles'),
    path('category/fashion/', views.category_filter, {'category': 'fashion'}, name='category_fashion'),
    path('category/gigs/', views.category_filter, {'category': 'gigs'}, name='category_gigs'),
    path('category/hiring/', views.category_filter, {'category': 'hiring'}, name='category_hiring'),
    path('category/electronics/', views.category_filter, {'category': 'electronics'}, name='category_electronics'),
    path('category/accessories/', views.category_filter, {'category': 'accessories'}, name='category_accessories'),
    path('category/health andbeauty/', views.category_filter, {'category': 'health and beauty'}, name='category_health and beauty'),
    path('category/luxury/', views.category_filter, {'category': 'luxury'}, name='category_luxury'),
    path('category/real estate/', views.category_filter, {'category': 'real estate'}, name='category_real estate'),
    path('category/food and drinks/', views.category_filter, {'category': 'food and drinks'}, name='category_food and drinks'),
    path('category/furniture/', views.category_filter, {'category': 'furniture'}, name='category_furniture'),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)