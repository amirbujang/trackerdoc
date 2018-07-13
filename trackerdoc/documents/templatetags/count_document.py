from django import template

from documents.models import Document

register = template.Library()

@register.filter()
def countdocument_by_status(template, comma_split_args):
    args = comma_split_args.split(",")
    count = ""
    if len(args) == 4:
        state, year, month, day = comma_split_args.split(",")
        count = Document.objects.filter(template__id=template.id, documentstate__created_at__year=year, documentstate__created_at__month=month, documentstate__created_at__day=day, documentstate__state__id=state).distinct().count()
    elif len(args) == 3:
        state, year, month = comma_split_args.split(",")
        count = Document.objects.filter(template__id=template.id, documentstate__created_at__year=year, documentstate__created_at__month=month, documentstate__state__id=state).distinct().count()
    elif len(args) == 2:
        state, year = comma_split_args.split(",")
        count = Document.objects.filter(template__id=template.id, documentstate__created_at__year=year, documentstate__state__id=state).distinct().count()
    elif len(args) == 1:
        state = comma_split_args.split(",")
        count = Document.objects.filter(template__id=template.id, documentstate__state__id=state).distinct().count()

    if count == 0:
        count = ""
    return count

@register.filter()
def countdocument_y(template, year):
    return template.count_document_y(year)

@register.filter()
def totaldocument_by_status(template, comma_split_args):
    args = comma_split_args.split(",")
    if len(args) == 4:
        state, year, month, day = comma_split_args.split(",")
        return Document.objects.filter(documentstate__created_at__year=year, documentstate__created_at__month=month, documentstate__created_at__day=day, documentstate__state__id=state).count()
    elif len(args) == 3:
        state, year, month = comma_split_args.split(",")
        return Document.objects.filter(documentstate__created_at__year=year, documentstate__created_at__month=month, documentstate__state__id=state).count()
    elif len(args) == 2:
        state, year = comma_split_args.split(",")
        return Document.objects.filter(documentstate__created_at__year=year, documentstate__state__id=state).count()
    elif len(args) == 1:
        state = comma_split_args.split(",")
        return Document.objects.filter(documentstate__state__id=state).count()


@register.filter()
def totaldocument_y(template, year):
    return Document.objects.filter(documentstate__created_at__year=year, documentstate__state__code="serah").count()
