from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Post, Subscription, Category
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, get_object_or_404
from django.db.models import Exists, OuterRef
from django.contrib.auth.decorators import login_required
from django.core.cache import cache


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

    def get_object(self, queryset=None):
        cache_key = f'post-{self.kwargs["pk"]}'
        post = cache.get(cache_key, None)

        if not post:
            post = super().get_object(queryset=queryset)
            cache.set(cache_key, post)

        return post

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


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = get_object_or_404(Category, id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )
