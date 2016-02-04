from django.contrib import admin

from models import Submit, SubmitReceiver


class SubmitAdmin(admin.ModelAdmin):
    pass


class SubmitReceiverAdmin(admin.ModelAdmin):
    pass

admin.site.register(Submit, SubmitAdmin)
admin.site.register(SubmitReceiver, SubmitReceiverAdmin)
