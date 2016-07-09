from django.contrib import admin

from testovac.results.models import CustomResultsTable


class CustomResultsTableAdmin(admin.ModelAdmin):
    pass


admin.site.register(CustomResultsTable, CustomResultsTableAdmin)
