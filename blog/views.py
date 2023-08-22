from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post
posts = [
    {
        'author': 'Huang',
        'title': 'Blog Post 1',
        'content': 'no Content',
        'date_posted': 'Aug, 2018'
    },
    {
        'author': 'George',
        'title': 'Blog Post 2',
        'content': 'no Content',
        'date_posted': 'Aug, 2018'
    }
]

def home(request):
    context = {
        'posts': Post.objects.all(),
        'title': 'blog'
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = '-date_posted'
    paginate_by = 5 # give paignation function


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5  # give paignation function

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

# LoginRequiredMixin used for login required for class do not have decorator
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    # for post-form 
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
# LoginRequiredMixin(login needed), UserPassesTestMixin(user needed)
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    # prevent update other posts
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    # prevent update other posts
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
