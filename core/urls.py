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
    path("explore", views.explore, name="explore"),

    path("", views.landing, name="landing"),
    path("user_profile/", views.user_profile, name="user_profile"),

    path("free_store/", views.free_store, name="free_store"),
    path("notification_list/", views.notification_list, name="notification_list"),
    path("settings/", views.settings_list, name="settings_list"),

    # path("profile/", views.profile, name="profile"),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)