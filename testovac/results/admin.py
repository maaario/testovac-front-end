from django.contrib import admin

from testovac.results.models import CustomResultsTable


class CustomResultsTableAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'number',)
    list_editable = ('number',)


admin.site.register(CustomResultsTable, CustomResultsTableAdmin)
