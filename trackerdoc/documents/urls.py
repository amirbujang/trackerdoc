from django.urls import path
from . import views

app_name = "documents"
urlpatterns = [
    path("", views.document_index, name="document_index"),
    path("view/<int:id>", views.document_view, name="view_document"),
    path("download/<int:id>", views.document_download, name="download_document"),
    path("edit/<int:id>", views.document_edit, name="edit_document"),
    path("delete/<int:id>", views.document_delete, name="delete_document"),
    path("create/", views.document_create, name="create_document"),
    path("update-state/", views.document_update_state, name="update_state"),
    path("track/<int:id>", views.track, name="track"),
    path("report/", views.report, name="report"),

    path("autocomplete/", views.autocomplete, name="autocomplete"),

    path("template/index/", views.template_index, name="template_index"),
    path("template/view/<int:id>", views.template_view, name="view_template"),
    path("template/create/", views.template_create, name="create_template"),
    path("template/edit/<int:id>/", views.template_edit, name="edit_template"),
    path("template/delete/<int:id>/", views.template_delete, name="delete_template"),
]
