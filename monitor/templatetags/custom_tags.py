#_*_coding:utf-8_*_
from django import template
from monitor import models
from django.utils.safestring import mark_safe
import time

register = template.Library()

@register.filter
def transform_time(value): # Only one argument.
    """transform time.time() to localtime()"""
    t = time.strftime('%Y-%m-%d:%H:%M', time.localtime(value))
    return t


@register.filter
def transform_dict(value):
    ret = ''
    if type(value) is dict:
        for k, v in value.items():
            ret += '<p>%s:%s</p>' % (k,v)
    else:
        ret = value
    return ret