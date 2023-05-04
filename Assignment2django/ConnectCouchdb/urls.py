from django.urls import path
from . import views

urlpatterns = [
    path('get_document_view/', views.get_document_view, name='get_document_view'),
    path('get_all_documents_view/', views.get_all_documents_view, name='get_all_documents_view'),
    path('get_document_view/<str:doc_id>/', views.get_document_view, name='get_document_view'),
    
]