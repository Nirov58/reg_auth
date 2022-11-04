from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from .models import Post
from .filters import NewsFilter
from .forms import NewsForm


class NewsList(ListView):
    model = Post
    ordering = '-date'
    template_name = 'news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsItem(DetailView):
    model = Post
    template_name = 'news_item.html'
    context_object_name = 'news_item'


class NewsSearch(NewsList):
    template_name = 'news_search.html'


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'news_portal_app.add_post'
    form_class = NewsForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        if 'news' in self.request.build_absolute_uri():
            news.type = Post.news
            print('new')
        elif 'article' in self.request.build_absolute_uri():
            news.type = Post.article
            print('art')
        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'news_portal_app.change_post'
    form_class = NewsForm
    model = Post
    template_name = 'news_create.html'
    context_object_name = 'news_create'


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')
