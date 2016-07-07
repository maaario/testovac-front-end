import re
from itertools import chain

from django import template
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from wiki.models import URLPath

register = template.Library()


def static_menu_items(request):
    items = [
        {
            'url_regex': r'^/news',
            'text': _('News'),
            'link': reverse('news_list', kwargs={'page': 1}),
        },
        {
            'url_regex': r'^/tasks',
            'text': _('Tasks'),
            'link': reverse('contest_list'),
        },
    ]

    if request.user.is_staff:
        items.append({
            'url_regex': r'^/admin',
            'text': 'Admin',
            'link': reverse('admin:index'),
        })

    return items


def wiki_articles_in_menu(request):
    wiki_root = URLPath.objects.filter(slug=None, site=get_current_site(request))
    first_level_urls = URLPath.objects.filter(parent=wiki_root)
    items = []

    for url in list(chain(wiki_root, first_level_urls)):
        if url.article.can_read(request.user):
            items.append({
                'url_regex': r'^' + url.article.get_absolute_url() + ('$' if url in wiki_root else ''),
                'text': url.article.current_revision.title,
                'link': url.article.get_absolute_url(),
            })

    return items


@register.inclusion_tag('menu/menu.html', takes_context=True)
def menu(context):
    request = context.get('request')
    items = static_menu_items(request) + wiki_articles_in_menu(request)
    for item in items:
        item['is_active'] = bool(re.search(item['url_regex'], request.path))
    return {'items': items}
