from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.forms import Widget
from django.utils.html import format_html

from models import SubmitReceiverTemplate, SubmitReceiver, Submit, Review


class SubmitReceiverTemplateAdmin(admin.ModelAdmin):
    pass


class LoadConfigurationFromTemplate(forms.Select):
    class Media:
        js = ('submit/load-configuration-from-template.js', )


class JSONEditorWidget(Widget):
    def render(self, name, value, attrs=None):
        return format_html('<div id="editor_holder"></div>')

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            '//maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js',
            'submit/jsoneditor.min.js',
            'submit/jsoneditorwidget.js',
        )

        css = {
            'all': ('//maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css', ),
        }


class SubmitReceiverForm(forms.ModelForm):
    receiver_template = forms.ChoiceField(
        choices=((x.id, str(x)) for x in SubmitReceiverTemplate.objects.all()),
        widget=LoadConfigurationFromTemplate()
    )

    class Meta:
        model = SubmitReceiver
        fields = ('receiver_template', 'configuration')
        widgets = {
            'configuration': JSONEditorWidget(),    # forms.Textarea(attrs={'rows': 15, 'cols': 40})
        }


class SubmitReceiverAdmin(admin.ModelAdmin):
    form = SubmitReceiverForm


class ReviewInline(admin.StackedInline):
    model = Review
    fields = ('time', 'score', 'short_response', 'comment', 'filename')
    readonly_fields = ('time',)
    ordering = ('-time',)
    extra = 0


class ViewOnSiteMixin(object):
    def view_on_site_list_display(self, obj):
        return mark_safe(u'<a href="{}">{}</a>'.format(obj.get_absolute_url(), 'view on site'))
    view_on_site_list_display.allow_tags = True
    view_on_site_list_display.short_description = u'View on site'


class SubmitAdmin(ViewOnSiteMixin, admin.ModelAdmin):
    inlines = [ReviewInline]
    list_display = ('submit_id', 'view_on_site_list_display', 'receiver', 'user', 'status', 'score', 'time',
                    'is_accepted')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

    def submit_id(self, submit):
        return 'submit %d' % (submit.id,)

    def status(self, submit):
        review = submit.last_review()
        return review.short_response if review is not None else ''

    def score(self, submit):
        review = submit.last_review()
        return review.display_score() if review is not None else ''


class ReviewAdmin(admin.ModelAdmin):
    pass

admin.site.register(SubmitReceiverTemplate, SubmitReceiverTemplateAdmin)
admin.site.register(SubmitReceiver, SubmitReceiverAdmin)
admin.site.register(Submit, SubmitAdmin)
admin.site.register(Review, ReviewAdmin)
