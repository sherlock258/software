"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import  url
from django.urls import path
from demo import views
from djangoProject import  settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.hello),
    path('media/<path>',serve,{'document_root':settings.MEDIA_ROOT}),
    url(r'^api/login$',views.login,name='login'),
    url(r'^api/register$', views.register, name='register'),
    url(r'^api/sendmail$', views.sendemail, name='sedmmail'),
    url(r'^api/userupdate$', views.userupdate, name='userupdate'),
    url(r'^api/userarticle', views.userarticle, name='userarticle'),
    url(r'^api/getarticle', views.getarticle, name='getarticle'),
    url(r'^api/selectkind', views.selectkind, name='selectkind'),
    url(r'^api/articleid', views.articleid, name='articleid'),
    url(r'^api/publish$', views.publish, name='publish'),
    url(r'^api/uploadpic$', views.uploadpic, name='uploadpic'),
    url(r'^api/selinlike', views.select_in_like, name='selinlike'),
    url(r'^api/selallinlike', views.select_all_like, name='selallinlike'),
    url(r'^api/collect', views.collect, name='collect'),
    url(r'^api/uncollect', views.uncollect, name='uncollect'),
    url(r'^api/selinattention', views.select_in_attention, name='selinattention'),
    url(r'^api/attention', views.attention, name='attention'),
    url(r'^api/unattention', views.unattention, name='unattention'),
    url(r'^api/getattention', views.getattention, name='getattention'),
    url(r'^api/articledel', views.article_del, name='articledel'),
    url(r'^api/articledel', views.article_del, name='articledel'),
    url(r'^api/getdraft', views.getdraft, name='getdraft'),
    url(r'^api/draft', views.draft_pub, name='draft'),
    url(r'^api/search', views.search, name='search'),
    url(r'^api/getcomment', views.getcomment, name='getcomment'),
    url(r'^api/addcomment', views.addcomment, name='addcomment'),
    url(r'^api/delcomment', views.delcomment, name='delcomment'),
]
