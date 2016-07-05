from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.utils.translation import ugettext as _


class CustomAdminSite(AdminSite):
    def index(self, request, extra_context=None):
        """
        Put `wiki images` and `wiki attachments` into a single tab `wiki` in admin:index view.
        """
        response = super(CustomAdminSite, self).index(request)
        apps = response.context_data['app_list']

        to_change = {'wiki': None, 'wiki_images': None, 'wiki_attachments': None}
        for app in apps:
            label = app['app_label']
            if label in to_change:
                to_change[label] = app

        if to_change['wiki'] is None or to_change['wiki_images'] is None or to_change['wiki_attachments'] is None:
            return response

        to_change['wiki']['models'].extend(to_change['wiki_attachments']['models'])
        to_change['wiki']['models'].extend(to_change['wiki_images']['models'])
        apps.remove(to_change['wiki_attachments'])
        apps.remove(to_change['wiki_images'])

        return response

admin.site = CustomAdminSite()

admin.site.site_header = _('Tester-site administration')
