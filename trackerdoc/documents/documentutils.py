from django.core.paginator import Paginator
from .models import Document

def search_documents(request):
    """Search documents by GET request (keyword, status_code and page)"""

    keyword = request.GET.get("keyword")
    status_code = request.GET.get("status_code")
    page = request.GET.get("page")

    if not keyword:
        keyword = ""

    keyword = keyword.strip()
    records = Document.search(keyword, status_code).order_by("-created_at").distinct()

    paginator = Paginator(records, 10)
    return paginator.get_page(page)


def documents_to_table(documents):
    """Transform List[Document] to html """
    table_headers = DocumentTableColumn.objects.all().order_by("sorting_order")
    rows = []
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
