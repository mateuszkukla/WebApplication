from django.urls import path, include
import web.views as views


urlpatterns = [
    path('', views.index, name="index")
    ]