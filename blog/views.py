from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import CreateUpdateForm
from django.views import generic
from django.urls import reverse_lazy


# Show all posts
class PostListView(generic.ListView):
    template_name = 'blog/posts_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(status='pub').order_by('-datetime_modified')


# Detail posts
class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


#


# Create post
class PostCreateView(generic.CreateView):
    form_class = CreateUpdateForm
    template_name = 'blog/post_create.html'


# Update posts
class PostUpdateView(generic.UpdateView):
    model = Post
    form_class = CreateUpdateForm
    template_name = 'blog/post_update.html'


# Delete post
class PostDeleteView(generic.DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('all_posts')
