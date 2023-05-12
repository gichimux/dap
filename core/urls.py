from django.urls import  path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [ 
    path("", views.home, name="home"),
    path("post-detail/", views.post_detail, name="post_detail"),
    path("about/", views.about, name="about"),
    path("login/", views.login, name="login"),
    path("profile/", views.profile, name="profile"),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)