"""rango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

from django.urls import path
from rango import views

app_name = 'rango'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('category/<slug:category_name_slug>/',
        views.ShowCategoryView.as_view(), name='show_category'),
    path('add_category/', views.AddCategoryView.as_view(), name='add_category'),
    path('category/<slug:category_name_slug>/add_page/', views.AddPageView.as_view(), name='add_page'),
    path('login_check/', views.LoginCheckView.as_view(), name='login_check'),
    #path('search/', views.search, name='search'),
    path('goto/', views.GoToUrl.as_view(), name='goto'),
    path('register_profile/', views.RegisterProfileView.as_view(), name='register_profile')
]

'''
This code imports the relevant Django machinery for URL mappings and the views
module from rango . This allows us to call the function url and point to the index
view for the mapping in urlpatterns .
'''