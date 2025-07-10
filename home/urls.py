from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.HomeView.as_view(), name = 'home'),
    path('post/<int:post_id>/<slug:post_slug>/', views.PostDetailView.as_view(), name = 'post_details'),
    path('post/delete/<int:post_id>/', views.PostDetailView.as_view(), name = 'post_delete'),
    path('post/update/<int:post_id>/', views.PostUpdateCreateForm, name = 'post_update'),
    path('post/create/', views.PostUpdateCreateForm, name = 'post_create')
]