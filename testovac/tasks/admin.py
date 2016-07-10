from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from testovac.submit.models import SubmitReceiver, SubmitReceiverTemplate
from testovac.tasks.models import Competition, Contest, Task


class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'get_users_group', 'get_admins_group', 'is_public')

    def get_users_group(self, competition):
        return competition.users_group
    get_users_group.short_description = _("official contestants' group")

    def get_admins_group(self, competition):
        if competition.administrators_group is None:
            return _('all staff')
        else:
            return competition.administrators_group
    get_admins_group.short_description = _("administrators' group")

    def is_public(self, competition):
        return competition.public
    is_public.boolean = True


class TaskInline(admin.TabularInline):
    model = Task
    extra = 0
    show_change_link = True
    readonly_fields = ('submit_receivers',)


class ContestAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'start_time', 'end_time', 'visible')
    list_editable = ('visible', )
    inlines = [TaskInline]

    def save_formset(self, request, form, formset, change):
        """
        Create default receivers for tasks when creating contest.
        """
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            try:
                if not change:
                    template = SubmitReceiverTemplate.objects.get(name=settings.TASKS_DEFAULT_SUBMIT_RECEIVER_TEMPLATE)
                    receiver = SubmitReceiver.objects.create(configuration=template.configuration)
                    instance.submit_receivers.add(receiver)
            finally:
                instance.save()
        formset.save_m2m()


class ReceiverInline(admin.TabularInline):
    model = Task.submit_receivers.through
    extra = 0

    readonly_fields = ('get_receiver_configuration',)

    def get_receiver_configuration(self, obj):
        return obj.submitreceiver.configuration
    get_receiver_configuration.short_description = 'configuration'


class TaskAdmin(admin.ModelAdmin):
    exclude = ('submit_receivers', )
    list_display = ('slug', 'name', 'number', 'contest', 'max_points')
    list_filter = ('contest', )
    search_fields = ('name', 'slug')
    inlines = [
        ReceiverInline,
    ]


admin.site.register(Competition, CompetitionAdmin)
admin.site.register(Contest, ContestAdmin)
admin.site.register(Task, TaskAdmin)
