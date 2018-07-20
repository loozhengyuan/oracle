from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('step1/', views.step1, name='step1'),
    path('step2/', views.step2, name='step2'),
    path('step3/', views.step3, name='step3')
]