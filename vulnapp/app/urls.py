from django.urls import path
from .views import RegisterView, LoginView, BoardPostsListView, BoardPostsCreateView, BoardPostsDeleteView, read_file_view, get_exif_data

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('', BoardPostsListView.as_view(), name='main'),
    path('create/', BoardPostsCreateView.as_view(), name='message-post'),
    path('delete/<int:pk>', BoardPostsDeleteView.as_view(), name='message-delete'),
    path('user_uploads/<str:file_name>', read_file_view, name='user-content-serve'),
    path('get_exif_data/<str:file_name>', get_exif_data, name='exif-data'),
]
