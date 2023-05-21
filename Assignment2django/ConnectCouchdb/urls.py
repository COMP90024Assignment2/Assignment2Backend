from django.urls import path
from . import views

urlpatterns = [
    
    path('get_all_documents_view/<str:type>/<str:dbname>/', views.get_all_documents_view, name='get_all_documents_view'),
    path('get_document_view/<str:type>/<str:dbname>/<str:doc_id>/', views.get_document_view, name='get_document_view'),
    path('create_document_view/<str:type>/<str:dbname>/', views.create_document_view, name='create_document_view'),
    path('create_multiple_documents_view/<str:type>/<str:dbname>/', views.create_multiple_documents_view, name='create_multiple_documents_view'),
    path('add_database_to_server/<str:type>/', views.add_database_to_server, name='add_database_to_server'),
    path('update_document_view/<str:type>/<str:dbname>/<str:doc_id>/', views.update_document_view, name='update_document_view'),
    path('delete_document_view/<str:type>/<str:dbname>/<str:doc_id>/', views.delete_document_view, name='delete_document_view'),
    path('mongodb_query_view/<str:type>/<str:dbname>/', views.mongodb_query_view, name='mongodb_query_view'),
    path('mongodb_key_query_view/<str:type>/<str:dbname>/<str:key>/', views.mongodb_key_query_view, name='mongodb_key_query_view'),
    path("upload_twitter_from_file_to_corresponding_couchdb/<str:type>/", views.upload_twitter_from_file_to_corresponding_couchdb, name="upload_twitter_from_file_to_corresponding_couchdb"),
    path("get_mapreduce_result_view/<str:type>/<str:homelessRelatedDbname>/<str:comparedDbname>/", views.get_mapreduce_result_view, name="get_mapreduce_result_view"),
    path("create_new_mastodon_mapreduce_view/<str:type>/<str:dbname>/", views.create_new_mastodon_mapreduce_view, name="create_new_mastodon_mapreduce_view"),
    path("get_mastodon_mapreduce_result_view/<str:type>/<str:dbname>/", views.get_mastodon_mapreduce_result_view, name="get_mastodon_mapreduce_result_view"),
]