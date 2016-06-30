from django.contrib import admin

from models import SubmitReceiverTemplate, SubmitReceiver, Submit, Review


class SubmitReceiverTemplateAdmin(admin.ModelAdmin):
    pass


class SubmitReceiverAdmin(admin.ModelAdmin):
    pass


class ReviewInline(admin.StackedInline):
    model = Review
    fields = ('time', 'score', 'short_response', 'comment', 'filename')
    readonly_fields = ('time',)
    ordering = ('-time',)
    extra = 0


class SubmitAdmin(admin.ModelAdmin):
    inlines = [ReviewInline]


class ReviewAdmin(admin.ModelAdmin):
    pass


admin.site.register(SubmitReceiverTemplate, SubmitReceiverTemplateAdmin)
admin.site.register(SubmitReceiver, SubmitReceiverAdmin)
admin.site.register(Submit, SubmitAdmin)
admin.site.register(Review, ReviewAdmin)
