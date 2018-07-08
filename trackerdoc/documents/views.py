from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.forms import formset_factory
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.template import Template, Context, loader

from weasyprint import HTML, CSS
from io import BytesIO
import datetime

from .models import DocumentTableColumn, Document, Data, DocumentState, TemplateTag

@login_required
def document_index(request):
    keyword = request.GET.get("keyword")
    status_code = request.GET.get("status_code")
    page = request.GET.get("page")

    if not keyword:
        keyword = ""

    keyword = keyword.strip()
    records = Document.search(keyword, status_code).order_by("-created_at").distinct()

    paginator = Paginator(records, 10)
    documents = paginator.get_page(page)

    table_headers = DocumentTableColumn.objects.all().order_by("sorting_order")
    for i, document in enumerate(documents):
        documents[i].columns = []
        for header in table_headers:
            if header.table == "data":
                tags = header.values.split(",")
                cell = Data.objects.filter(document__id=document.id, template_tag__tag__in=tags).first()
                if cell:
                    documents[i].columns.append(cell.content)
                else:
                    documents[i].columns.append('')
            elif header.table == "state":
                cell = DocumentState.objects.filter(document__id=document.id, state__code=header.values).last()
                if cell:
                    documents[i].columns.append(cell.created_at)
                else:
                    documents[i].columns.append('')


    return render(request, "documents/document_index.html", {"documents": documents, "table_headers": table_headers, "keyword": keyword})


from .forms import DataForm
@login_required
def document_create(request):
    tags = TemplateTag.objects.all()

    initials = []
    for tag in tags:
        initials.append({'template_tag': tag.id})

    DataFormSet = formset_factory(DataForm, extra=0)
    formset = DataFormSet(initial=initials)
    return render(request, "documents/document_create.html", {"formset": formset, 'template_tags': tags})

@login_required
def document_edit(request, id):
    return HttpResponse("edit document")

@login_required
def document_delete(request, id):
    return HttpResponse("delete document")

@login_required
def document_download(request, id):
    return HttpResponse("download document")
