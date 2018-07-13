from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

class DocumentTableColumn(models.Model):
    header = models.CharField(max_length=50)
    table = models.CharField(max_length=50)
    values = models.TextField()
    sorting_order = models.IntegerField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.header

class State(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    narration = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=20)
    source = models.ForeignKey(State, on_delete=models.CASCADE, related_name="source")
    destination = models.ForeignKey(State, on_delete=models.CASCADE, related_name="destination")
    sorting_order = models.IntegerField(default=99)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Template(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    template_single_page = models.TextField(blank=True)
    template_with_attachment = models.TextField(blank=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def count_document_ym(self, year, month):
        return Document.objects.filter(documentstate__created_at__month=month, documentstate__created_at__year=year, template__id=self.id, documentstate__state__code="serah").count()

    def count_document_y(self, year):
        return Document.objects.filter(documentstate__created_at__year=year, template__id=self.id, documentstate__state__code="serah").count()

class TemplateTag(models.Model):
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    tag = models.CharField(max_length=50)
    label = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=20)
    default_content = models.TextField(blank=True)
    is_searchable = models.BooleanField(default=False)
    is_capitalize = models.BooleanField(default=True)
    is_autocomplete = models.BooleanField(default=False)
    sorting_order = models.IntegerField(default=99)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s.%s [%d]" % (self.template.name, self.tag, self.sorting_order,)

class Document(models.Model):
    name = models.CharField(max_length=100)
    note = models.TextField(blank=True)
    current_state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    template = models.ForeignKey(Template, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    columns = []

    def __str__(self):
        return self.name

    def search(keyword, status_code):
        q = Document.objects.filter(
             data__content__contains=keyword,
             data__template_tag__is_searchable=True
        )

        if status_code:
            q = q.filter(current_state__code=status_code)

        return q

    def last_state(self):
        return self.documentstate_set.order_by("created_at").last()

    def events(self):
        if self.current_state:
            events = Event.objects.filter(source__id=self.current_state.id).order_by('sorting_order').all()
            return events

        return []

class Data(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    template_tag = models.ForeignKey(TemplateTag, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['template_tag__sorting_order']

    def __str__(self):
        return "%s.%s : %s" % (self.document.name, self.template_tag.tag, self.content,)

class DocumentState(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True, editable=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at.editable=True

    def __str__(self):
        return "%s.%s" % (self.document.name, self.state.name, )
