from django.urls import path, include

from .views import home_page_view, login_page, log_out_page, select_food, add_food, register_page, profile_page, update_food, \
    delete_food
urlpatterns = [
    path('', home_page_view, name='home'),
    path('login/', login_page, name='login'),
    path('logout/', log_out_page, name='logout'),
    path('select_food/', select_food, name='select_food'),
    path('add_food/', add_food, name='add_food'),
    path('update_food/<str:pk>/', update_food, name='update_food'),
    path('delete_food/<str:pk>/', delete_food, name='delete_food'),
    path('register/', register_page, name='register'),
    path('profile/', profile_page, name='profile'),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),

]
