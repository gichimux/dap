from django.urls import  path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [ 
    path("home/", views.home, name="home"),
    path("home/post_detail/<int:id>", views.post_detail, name="post_detail"),
    path("home/chats/", views.chat_list, name="chat_list"),
    path("delete_post/<int:id>", views.delete_post, name="delete_post"),

    path("home/baraza", views.baraza, name="baraza"),
    path("home/explore", views.explore, name="explore"),

    path("", views.landing, name="landing"),
    path("@<str:profile_username>", views.view_profile, name="view_profile"),
    
    path("follow/@<str:profile_username>/",views.follow_toggle, name="follow_toggle"),
    path("@<str:profile_username>/following", views.follow_list, name="follow_list"),
    # path("like/<int:post_id>/",views.like_toggle, name="like_toggle"),
    path("like",views.like_button, name="like_button"),
    path("search/", views.post_search, name="search_results"),

    path("free_store/", views.free_store, name="free_store"),
    path("notification_list/", views.notification_list, name="notification_list"),
    path("settings/", views.settings_list, name="settings_list"),

    # path("profile/", views.profile, name="profile"),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)