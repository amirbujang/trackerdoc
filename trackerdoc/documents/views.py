from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.forms import inlineformset_factory, formset_factory
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.template import Template, Context, loader

from calendar import monthrange
from weasyprint import HTML, CSS
from io import BytesIO
import re, json

from .models import DocumentTableColumn, Document, Data, DocumentState, TemplateTag, Template, State
from .forms import DataForm, DocumentForm, TemplateForm, TemplateUploadForm, TemplateTagForm, StatusUpdateForm, ReportForm
from .date import get_today_date, get_today_local_date, get_today_hijri_date
from .documentutils import search_documents, search_document
from .utils import reportutils

def make_filename_safe(name):
    regex = re.compile('[^a-zA-Z0-9 ]')
    return regex.sub('', name)

@login_required
def document_index(request):
    template_id = request.GET.get("template_id")
    template = None
    if template_id:
        template = Template.objects.filter(id=template_id).first()

    documents = search_documents(request)


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

            elif header.table == "state_data":
                cell = DocumentState.objects.filter(document__id=document.id).last()
                if cell:
                    documents[i].columns.append(cell.extra_data)

    states = State.objects.all()
    templates = Template.objects.filter(is_active=True).all()
    navbar_templates = templates
    return render(request, "documents/document_index.html", {"documents": documents, "table_headers": table_headers, "templates": templates, "states": states, 'template': template, 'navbar_templates': navbar_templates})

@login_required
def document_create(request):
    template_id = request.GET.get('template_id')
    template = Template.objects.filter(id=template_id).first()
    tags = TemplateTag.objects.filter(template__id=template_id).order_by('sorting_order').all()
    DataFormSet = inlineformset_factory(Document, Data, form=DataForm, extra=len(tags), can_delete=False)

    if request.method == "POST":
        baru = State.objects.filter(type="start").first()
        document = Document()
        document.template = template
        document.current_state = baru
        document.save()
        document.documentstate_set.create(
            state=document.current_state,
            user=request.user
        )

        formset = DataFormSet(request.POST, instance=document)
        if formset.is_valid():
            formset.save()

            data = Data.objects.filter(document__id=document.id, template_tag__tag=document.template.filename_tag).first()
            doc = Document.objects.filter(id=document.id).first()
            doc.name = make_filename_safe(data.content)
            doc.save()

            return HttpResponseRedirect(reverse('documents:document_index'))

    else:
        initials = []
        for tag in tags:
            data = {'template_tag': tag.id, 'content': ''}
            if tag.type == 'local_date':
                data["content"] = get_today_local_date()
            elif tag.type == 'hijri_date':
                data["content"] = get_today_hijri_date()
            elif tag.type == 'date':
                data["content"] = get_today_date()

            if tag.default_content:
                data["content"] = tag.default_content

            if tag.is_capitalize and data["content"]:
                data["content"] = data["content"].upper()

            initials.append(data)

        formset = DataFormSet(initial=initials)

    navbar_templates = Template.objects.filter(is_active=True).all()
    return render(request, "documents/document_create.html", {"formset": formset, 'template_tags': tags, "template_id": template_id, 'template': template, 'navbar_templates': navbar_templates})


@login_required
def document_edit(request, id):
    document = Document.objects.filter(id=id).first()
    tags = TemplateTag.objects.filter(template_id=document.template.id).order_by('sorting_order').all()
    DataFormSet = inlineformset_factory(Document, Data, form=DataForm, extra=0, can_delete=False)

    if request.method == "POST":
        formset = DataFormSet(request.POST, instance=document)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(reverse('documents:document_index'))

    else:
        formset = DataFormSet(instance=document)

    navbar_templates = Template.objects.filter(is_active=True).all()
    return render(request, "documents/document_edit.html", {"formset": formset, 'template_tags': tags, 'document': document, 'navbar_templates': navbar_templates})

@login_required
def document_view(request, id):
    document = Document.objects.filter(id=id).first()
    html = document.template.template_single_page

    dataset = Data.objects.filter(document__id=document.id).all()
    for data in dataset:
        tag = data.template_tag
        html = html.replace(tag.tag, data.content)

    # return HttpResponse(html)
    return render(request, "documents/template.html")

@login_required
def document_delete(request, id):
    document = Document.objects.filter(id=id).first()
    document.delete()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def document_download(request, id):
    document = Document.objects.filter(id=id).first()
    html = document.template.template_single_page

    dataset = Data.objects.filter(document__id=document.id).all()
    for data in dataset:
        tag = data.template_tag
        if tag.is_capitalize:
            data.content = data.content.upper()

        html = html.replace(tag.tag, data.content)

    pdf_file = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')

    filename = document.name
    response['Content-Disposition'] = 'filename="%s.pdf"' % (filename, )
    return response

@login_required
def document_update_state(request):
    data = request.POST["documents"]
    forms = json.loads(data)

    for form in forms:
        document = Document.objects.filter(id=form["document_id"]).first()
        state = State.objects.filter(id=form["destination_id"]).first()
        data = form["data"]
        docstate = DocumentState(document=document, state=state, extra_data=data, user=request.user)
        docstate.save()
        document.current_state = state
        document.save()

    return HttpResponse(data)

@login_required
def template_index(request):
    templates = Template.objects.all()
    navbar_templates = Template.objects.filter(is_active=True).all()
    return render(request, "documents/template_index.html", {"templates": templates, 'navbar_templates': navbar_templates})

@login_required
def template_view(request, id):
    template = Template.objects.filter(id=id).first()
    return HttpResponse(template.template_single_page)

@login_required
def template_create(request):
    if request.method == "POST":
        form = TemplateUploadForm(request.POST, request.FILES)
        if form.is_valid():
            template = form.save(commit=False)
            html = request.FILES['html_template'].read().decode("windows-1252")
            template.template_single_page = html
            template.save()
            return HttpResponseRedirect(reverse("documents:edit_template",  kwargs={'id':template.id}))
        else:
            return HttpResponse("form not valid")
    else:
        form = TemplateUploadForm()
        navbar_templates = Template.objects.filter(is_active=True).all()
        return render(request, "documents/template_create.html", {"form": form, 'navbar_templates': navbar_templates})


@login_required
def template_edit(request, id):
    template = Template.objects.filter(id=id).first()
    tags = re.findall('(__.*?__)', template.template_single_page)
    tags_set = set()
    tags_list = []
    for tag in tags:
        if tag not in tags_set:
            tags_list.append(tag)
            tags_set.add(tag)

    current_count = TemplateTag.objects.filter(template__id=id).count()
    extra = len(tags_set) - current_count

    TagFormSet = inlineformset_factory(Template, TemplateTag, form=TemplateTagForm, can_delete=True, extra=extra)

    if request.method == "POST":
        form = TemplateForm(request.POST, instance=template)
        if form.is_valid():
            form.save()
            formset = TagFormSet(request.POST, instance=template)
            if formset.is_valid():
                formset.save()

            return HttpResponseRedirect(reverse("documents:template_index"))
        else:
            return HttpResponse("form not valid")
    else:
        form = TemplateForm(instance=template)
        initials = []
        for tag in tags_list:
            initials.append({'tag': tag})

        formset = TagFormSet(initial=initials, instance=template)

        navbar_templates = Template.objects.filter(is_active=True).all()
        return render(request, "documents/template_edit.html", {"form": form, "formset": formset, 'navbar_templates': navbar_templates})


@login_required
def template_delete(request, id):
    template = Template.objects.filter(id=id).first()
    template.delete()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def report(request):
    parent_templates = Template.get_parents()
    data = []
    totals = []
    years = []
    grand_total = 0

    if request.GET:
        form = ReportForm(request.GET)
    else:
        form = ReportForm()

    if form.is_valid():
        data = form.cleaned_data
        report_type = data['report_type']
        status = data['status']
        year = data['year']

        if report_type == "monthly":
            data, totals = reportutils.get_total_by_month(parent_templates, status, year)
            grand_total = sum(totals)
        elif report_type == "yearly":
            data, totals = reportutils.get_total_by_year(parent_templates, status)
            grand_total = sum(totals)
            years = reportutils.get_years()

    else:
        report_type = ''

    return render(request, "documents/report.html", {
            'form': form,
            'report_type': report_type,
            'parents': parent_templates,
            'data': data,
            'years': years,
            'totals': totals,
            'grand_total': grand_total
        })

def track(request, id):
    documents = Document.objects.filter(id=id).all()
    table_headers = DocumentTableColumn.objects.all().order_by("sorting_order")
    return render(request, "documents/track.html", {"documents": documents, "table_headers": table_headers})


@login_required
def autocomplete(request):
    tag = request.GET.get("tag");
    kw = request.GET.get("kw");

    datas = Data.objects.values_list('content').filter(template_tag__tag=tag, content__contains=kw).distinct()[:3]
    result = [d[0] for d in datas]
    return JsonResponse(result, safe=False)


def public_check(request):
    documents = search_document(request)

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

            elif header.table == "state_data":
                cell = DocumentState.objects.filter(document__id=document.id).last()
                if cell:
                    documents[i].columns.append(cell.extra_data)

    states = State.objects.all()
    templates = Template.objects.filter(is_active=True).all()
    navbar_templates = templates
    return render(request, "documents/public_check.html", {
        "documents": documents,
        "table_headers": table_headers,
        "states": states,
    })
