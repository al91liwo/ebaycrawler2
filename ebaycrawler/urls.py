"""ebaycrawler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path

from data.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', EbayUserListView.as_view(), name='user_list'),
    path('delete-user/<pk>', delete_user, name='delete_user'),
    path('update', update_user, name='update_user'),
    path('templates', templates, name='templates'),
    path('add_email_template/<pk>', add_email_template, name='add_email_template'),
    path('download/<path>', download, name='download'),
    path('add_pdf_template', add_pdf_template, name='add_pdf_template'),
    path('add_new_email_template', add_new_email_template, name='add_new_email_template'),
    path('send', send, name='send'),
    path('sending', sending, name='sending'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('dies/', dies, name='dies')
]
