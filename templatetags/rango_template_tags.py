from django import template
from tango.models import Category


register = template.Library()

@register.inclusion_tag('tango.cats.html')
def get_category_list():
    return {'cats':Category.objects.all()}