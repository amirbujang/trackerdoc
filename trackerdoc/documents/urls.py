from django.urls import path
from . import views

app_name = "documents"
urlpatterns = [
    path("", views.document_index, name="document_index"),
    path("download/<int:id>", views.document_download, name="download_document"),
    path("edit/<int:id>", views.document_edit, name="edit_document"),
    path("delete/<int:id>", views.document_delete, name="delete_document"),
    path("create/", views.document_create, name="create_document"),
]
