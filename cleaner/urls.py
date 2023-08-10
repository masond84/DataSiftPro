from django.urls import path
from . import views
from .views import FileRenameView

app_name = 'cleaner'
urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('files/', views.upload_and_list_files, name='file_list'),
    path('files/<int:pk>/', views.file_detail, name="file_detail"),
    path('delete_file/<int:file_id>/', views.delete_file, name="delete_file"),
    path('rename/<int:pk>/', FileRenameView.as_view(), name="rename_file"),
    path('save_file_content/', views.save_file_content, name="save_file_content"),
    ## Algorithms Url ##
    path('algorithms/', views.algorithms, name="algorithms"),
    path('ranking-script/', views.run_script_1, name="ranking_script"),
    path('download/<path:file_name>/', views.download_files, name="download_files"),
    path('download_algorithms/<int:file_id>/', views.download_algorithms, name="download_algorithms"),
    ## Keyword Functionality ##
    path('keywords/', views.add_keywords_weights, name="add_keywords"),
    path('save_keywords/', views.save_keywords, name="save_keywords"),
    path('clear_keywords/', views.clear_keywords, name="clear_keywords"),
]
