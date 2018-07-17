# -*- coding: utf-8 -*-

from django import template
from ..utils import smartify_language, translit
from ..models import Country
from django.utils import translation

register = template.Library()


@register.filter
def smart_language(value):
    if isinstance(value, Country):
        if translation.get_language() == 'ru':
            return value.name_ru
        else:
            return value.name_en
    return smartify_language(value)


@register.filter
def force_translit(value):
    if translation.get_language() != 'ru':
        if isinstance(value, basestring):
            return  translit(value, 'ru', reversed=True)
    return value


@register.filter
def sanitize_tags(value):
    return value
    #TODO: remove all html tags from a string except some specific tags .