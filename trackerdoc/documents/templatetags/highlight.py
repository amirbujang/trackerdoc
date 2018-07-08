from django import template
from django.utils.safestring import mark_safe

import re

register = template.Library()

@register.filter()
def highlight(text, word):
    if len(word.strip()) == 0:
        return text

    result = re.sub(r'('+word+')', r'<span class="highlight">\1</span>', text, flags=re.IGNORECASE)
    return mark_safe(result)
