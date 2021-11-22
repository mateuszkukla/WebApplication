from django.urls import path, include
import web.views as views


urlpatterns = [
    path("", views.home, name="home"),
    # path("<int:id>", views.index, name="index"),
    # path("create/", views.create, name="create"),
    ]