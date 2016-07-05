from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from testovac.tasks.models import Competition, Contest, Task


class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_access_group')

    def get_access_group(self, obj):
        if obj.public:
            return _('all')
        else:
            return obj.users_group
    get_access_group.short_description = _('accessible for group')


class ContestAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'competition', 'start_time', 'end_time', 'is_visible')
    list_filter = ('competition', )

    def is_visible(self, obj):
        return obj.visible
    is_visible.boolean = True
    is_visible.short_description = _('visibility')


class ReceiverInline(admin.TabularInline):
    model = Task.submit_receivers.through
    extra = 0

    readonly_fields = ('get_receiver_configuration',)

    def get_receiver_configuration(self, obj):
        return obj.submitreceiver.configuration
    get_receiver_configuration.short_description = 'configuration'


class TaskAdmin(admin.ModelAdmin):
    exclude = ('submit_receivers', )
    list_display = ('name', 'number', 'contest', 'max_points')
    list_filter = ('contest', )
    search_fields = ('name', )
    inlines = [
        ReceiverInline,
    ]


admin.site.register(Competition, CompetitionAdmin)
admin.site.register(Contest, ContestAdmin)
admin.site.register(Task, TaskAdmin)
