"""OMBD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from OMBD_app.views import *


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    ##########login & registration start
    url(r'^$',display_login),
    url(r'^show_register',show_register,name="show_register"),
    url(r'^register', register, name="register"),
    url(r'^display_login', display_login, name="display_login"),
    url(r'^check_login', check_login, name="check_login"),
    url(r'^logout',logout,name="logout"),
    ##########login & registration end


    ################Admin start
    url(r'^show_home_admin',show_home_admin,name="show_home_admin"),
    url(r'^view_users_admin',view_users_admin,name="view_users_admin"),
    url(r'^get_requests_admin',get_requests_admin,name="get_requests_admin"),
    url(r'^approve',approve,name="approve"),
    url(r'^reject',reject,name="reject"),
    ################Admin end

    ###############User start
    url(r'^show_dmbd_user',show_dmbd_user,name="show_dmbd_user"),
    url(r'^go_to_verification',go_to_verification,name="go_to_verification"),
    url(r'^verify_key',verify_key,name="verify_key"),
    url(r'^upload_data_user',upload_data_user,name="upload_data_user"),
    url(r'^upload',upload,name="upload"),
    url(r'^get_images',get_images,name="get_images"),
    url(r'^send_mail',send_mail,name="send_mail"),
    url(r'^show_data_user',show_data_user,name="show_data_user"),
    url(r'^download',download,name="download"),
]
