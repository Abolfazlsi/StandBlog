from django.template import Library

register = Library()


@register.inclusion_tag("home/tag_result.html")
def show(queryset):
    return {"objects": queryset}
