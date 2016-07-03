from django.contrib import admin
from django import forms

from models import SubmitReceiverTemplate, SubmitReceiver, Submit, Review


class SubmitReceiverTemplateAdmin(admin.ModelAdmin):
    pass


class LoadConfigurationFromTemplate(forms.Select):
    class Media:
        js = ('submit/load-configuration-from-template.js', )


class SubmitReceiverForm(forms.ModelForm):
    receiver_template = forms.ChoiceField(
        choices=((x.id, str(x)) for x in SubmitReceiverTemplate.objects.all()),
        widget=LoadConfigurationFromTemplate()
    )

    class Meta:
        model = SubmitReceiver
        fields = ('receiver_template', 'configuration')
        widgets = {
            'configuration': forms.Textarea(attrs={'rows': 15, 'cols': 40})
        }


class SubmitReceiverAdmin(admin.ModelAdmin):
    form = SubmitReceiverForm


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
