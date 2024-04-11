from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy

class PostList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'news/index.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'news/details.html'
    context_object_name = 'new'

class PostCreate( PermissionRequiredMixin, CreateView ):
    permission_required = ('news.add_post')
    form_class = PostForm
    model = Post
    template_name = 'Post_edit.html'

    def form_valid(self, form):
       post = form.save(commit=False)
       if self.request.path == '/news/news/create/':
           post.categoryType = "NW"
           post.save()
       return super().form_valid(form)

class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    form_class = PostForm
    model = Post
    template_name = 'Post_edit.html'

class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    model = Post
    template_name = 'Post_delete.html'
    success_url = reverse_lazy('post_list')
