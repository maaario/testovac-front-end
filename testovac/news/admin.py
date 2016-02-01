from django.contrib import admin
from django.db import models

from easy_select2.widgets import Select2Multiple

from testovac.news.models import Entry


class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'author')
    exclude = ('author',)

    formfield_overrides = {
        models.ManyToManyField: {'widget': Select2Multiple()}
    }

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

admin.site.register(Entry, EntryAdmin)
