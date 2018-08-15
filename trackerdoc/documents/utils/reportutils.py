from documents.models import Document
from datetime import datetime

def get_total_by_month(parent_templates, status, year):
    parents = []
    month_totals = [0,0,0,0,0,0,0,0,0,0,0,0,0]
    for parent in parent_templates:
        totals = []
        subtotal = 0
        for month in range(1,13):
            total = Document.objects.filter(
                documentstate__state__id=status,
                documentstate__created_at__year=year,
                documentstate__created_at__month=month,
                template__parent=parent
                ).distinct().count()

            subtotal += total
            month_totals[month] += total
            totals.append(total)

        totals.append(subtotal)
        parents.append([parent, totals])

    return (parents, month_totals[1:])

def get_years():
    since_year = 2018
    current_year = datetime.now().year
    result = []
    for i in range(current_year - since_year + 1):
        result.append(since_year)
        since_year += 1

    return result

def get_total_by_year(parent_templates, status):
    parents = []
    since_year = 2018
    current_year = datetime.now().year

    year_totals = []
    for year in get_years():
        year_totals.append(0)

    for parent in parent_templates:
        totals = []
        subtotal = 0
        for i, year in enumerate(get_years()):
            total = Document.objects.filter(
                documentstate__state__id=status,
                documentstate__created_at__year=year,
                template__parent=parent
                ).distinct().count()

            subtotal += total
            year_totals[i] += total
            totals.append(total)

        totals.append(subtotal)
        parents.append([parent, totals])

    return (parents, year_totals)
