"""test_sign URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path,include
from sign import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('index/',views.index),
    path('login_action/',views.login_action),

    path('event_manage/',views.event_manage),
    path('event_manage/add_event/',views.add_event),
    path('event_manage/edit_event/<int:pid>/',views.edit_event),

    path('accounts/login/',views.index),
    path('logout/',views.logout),
    path('search_name/',views.search_name),
    path('search_phone/',views.search_phone),

    path('guest_manage/',views.guest_manage),
    path('guest_manage/add_guest/',views.add_guest),
    path('guest_manage/edit_guest/<int:pid>/',views.edit_guest),

    path('sign_index/<int:event_id>/',views.sign_index),
    path('sign_index_action/<int:event_id>/',views.sign_index_action),

    #接口
    path('api/',include('sign.urls')),

]
