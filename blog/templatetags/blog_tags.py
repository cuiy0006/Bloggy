from ..models import Post, Category, Tag
from django import template
from django.db.models.aggregates import Count

register = template.Library()

@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-created_time')[:num]

@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')

@register.simple_tag
def get_categories():
    #return Category.objects.all()
    #gt >; lt <; e ==
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gte=1)

@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gte=1)

@register.filter
def get_item(dic, key):
    return dic.get(key, [])

@register.filter
def list_has_element(dic, key):
    return key in dic