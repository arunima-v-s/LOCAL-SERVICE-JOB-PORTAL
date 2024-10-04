"""
URL configuration for jobportal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from owner import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name='home'),

    path('register',views.register_view,name='register'),
    path('login',views.login_view,name='login'),

    path('consumer/',include('consumer.urls')),
    path('worker/',include('worker.urls')),
    path('adminlogin', LoginView.as_view(template_name='owner/admin_login.html'),name='adminlogin'),

    path('afterlogin',views.afterlogin_view,name='afterlogin'),
    path('admin-dashboard',views.admin_dashboard_view,name='admin-dashboard'),

    path('worker-request',views.worker_request_view,name='worker-request'),
    path('approve-worker/<int:pk>',views.approve_worker_view,name='approve-worker'),
    path('admin-approve-worker',views.admin_approve_worker,name='admin-approve-worker'),
    path('reject-worker/<int:pk>',views.reject_worker_view,name='reject-worker'),

    path('manage-worker',views.manage_worker_view,name='manage-worker'),
    path('update-worker/<int:pk>',views.update_worker_view,name='update-worker'),
    path('delete-worker/<int:pk>',views.delete_worker_view,name='delete-worker'),

    path('manage-consumer',views.manage_consumer_view,name='manage-consumer'),
    path('update-consumer/<int:pk>',views.update_consumer_view,name='update-consumer'),
    path('delete-consumer/<int:pk>',views.delete_consumer_view,name='delete-consumer'),
]