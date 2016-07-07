from django.contrib import admin
from django.utils.translation import ugettext as _


def group_apps(app_list, main_app_label, grouped_apps_labels):
    """
    Put all models of `grouped_apps` into a single tab `main_app` in admin:index view.
    """
    selected_apps = {app: None for app in grouped_apps_labels + [main_app_label]}

    for app in app_list:
        label = app['app_label']
        if label in selected_apps:
            selected_apps[label] = app

    for app_label, app in selected_apps.items():
        if app is None:
            return

    for app_label in set(grouped_apps_labels) - {main_app_label}:
        selected_apps[main_app_label]['models'].extend(selected_apps[app_label]['models'])
        app_list.remove(selected_apps[app_label])


def admin_site_custom_index_view(request):
    response = admin.site.index(request)
    apps = response.context_data['app_list']
    group_apps(apps, 'wiki', ['wiki_attachments', 'wiki_images'])
    group_apps(apps, 'news', ['taggit'])
    return response

admin.site.site_header = _('Tester-site administration')
