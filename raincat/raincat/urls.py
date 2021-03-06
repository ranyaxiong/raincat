"""raincat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token
from forum import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/posts/$', views.PostList.as_view()),
    url(r'^api/v1/posts/(?P<pk>[0-9]+)/$', views.PostDetail.as_view()),
    url(r'^api/v1/users/$', views.UserList.as_view()),
    url(r'^api/v1/users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^api/v1/comments/$', views.CommentList.as_view()),
    url(r'^api/v1/comments/(?P<pk>[0-9]+)/$', views.CommentDetail.as_view()),
    url(r'^api/v1/profiles/$', views.UserProfile.as_view()),
    url(r'^login/$', views.LoginView.as_view()),
    url(r'^api-token-auth/', obtain_jwt_token),
]
urlpatterns = format_suffix_patterns(urlpatterns)
