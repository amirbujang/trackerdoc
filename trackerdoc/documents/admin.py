from django.contrib import admin

from .models import Document, Data, DocumentState, State, Event, Template, TemplateTag, DocumentTableColumn, EventPermission

admin.site.register(Document)
admin.site.register(Data)
admin.site.register(DocumentState)
admin.site.register(Template)
admin.site.register(TemplateTag)
admin.site.register(State)
admin.site.register(Event)
admin.site.register(EventPermission)
admin.site.register(DocumentTableColumn)
