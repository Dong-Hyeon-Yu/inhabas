from django import template

register = template.Library()


@register.simple_tag
def table_row_index(page, forloop_counter0):
    return page.start_index() + forloop_counter0
