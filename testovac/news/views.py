from django.views.generic import ListView

from testovac.news.models import Entry


class EntryListView(ListView):
    model = Entry
    template_name = 'news/index.html'
    context_object_name = 'news_entries'
    paginate_by = 10

    # def get_queryset(self):
    #     return self.model.objects.filter(
    #         competitions__id__exact=)
