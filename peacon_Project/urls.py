"""peacon_Project URL Configuration

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
from django.urls import path ,include
from peacon_app import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.index, name = 'index'),
    path('index', views.index, name = 'index'),
    path('', views.loginuser, name = 'loginuser'),
    path('register/<int:TypeRegist>', views.register, name = 'register'),
    path('agenda/<int:Date>', views.agenda, name = 'agenda'),
    path('virtual/<int:Room>', views.virtual, name = 'virtual'),
    path('paper/<int:Group>', views.paper, name = 'paper'),
    path('detail_paper/<int:papers>', views.detail_paper, name = 'detail_paper'),
    path('about/',views.about, name = 'about'),
    path('survey/',views.survey, name = 'survey'),
    path('contact/',views.contact, name = 'contact'),
    path('detail/<int:Papers>',views.detail,name = 'detail'),
    url(r'^ajax/validate_username/$', views.validate_username, name='validate_username'),
    path('check/',views.check, name = 'check'),
    path('check2/',views.check2, name = 'check2'),
    path('reset/',views.reset_password, name = 'reset_password'),
    path('game/',views.game, name = 'game'),
    path('health/', views.health, name="health"),
    path('export/', views.export_users_xls, name='export_users_xls'),
]+ static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)
