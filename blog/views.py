from urllib import request
from django.shortcuts import render, get_object_or_404, redirect
from users.models import User
from blog.models import TAG_OPTIONS
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from django import forms
from django.db.models import Q
from .forms import SubscriberForm
from .models import Subscriber
from django.utils import timezone

def subscribe(request):
    if request.method == "POST":
        email = request.POST.get("email", "").lower().strip()
        action = request.POST.get("action")

        if not email:
            messages.info(request, "Please enter a valid email.")
            return redirect(request.META.get("HTTP_REFERER", "/"))

        subscriber, created = Subscriber.objects.get_or_create(email=email)

        if action == "subscribe":
            subscriber.is_active = True
            subscriber.unsubscribed_at = None
            subscriber.save()
            messages.success(request, f"Successfully subscribed with email: {email}")

        elif action == "unsubscribe":
            subscriber.is_active = False
            subscriber.unsubscribed_at = timezone.now()
            subscriber.save()
            messages.success(request, f"You have been removed from the list with email: {email}")

    return redirect(request.META.get("HTTP_REFERER", "/"))

def services(request):
    return render(request, 'blog/services.html')

def main(request):
    context = {}
    context['posts'] = Post.objects.all()
    return render(request, 'blog/jose-dom-index.html', context=context)

def resume(request):
    return render(request, 'blog/resume.html')

class PostListView(ListView):
    model = Post
    template_name = 'blog/blog.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 6

    def get_context_data(self,**kwargs):
        context = super(PostListView,self).get_context_data(**kwargs)
        tags = TAG_OPTIONS
        first_tag = map(lambda x: x[0], tags)
        context['tags'] = first_tag
        return context
    
    def get_queryset(self):
        qs = super().get_queryset()
        q = (self.request.GET.get("q") or "").strip()
        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(content__icontains=q) |
                Q(tag__icontains=q)
            ).distinct()
        return qs

class TagPostListView(ListView):
    model = Post
    template_name = 'blog/blog.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 50

    def get_context_data(self,**kwargs):
        context = super(TagPostListView,self).get_context_data(**kwargs)
        tags = TAG_OPTIONS
        first_tag = map(lambda x: x[0], tags)
        context['tags'] = first_tag
        return context

    def get_queryset(self,**kwargs):
        return Post.objects.filter(tag__icontains=self.kwargs['tag'])

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'preview', 'read_time', 'content_html_file', 'content' ,'tag', 'featured_image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def clean_html_upload(self):
        f = self.cleaned_data.get("content_html_file")
        if not f:
            return None

        name = (f.name or "").lower()
        if not name.endswith((".html", ".htm")):
            raise forms.ValidationError("Please upload an .html or .htm file.")

        # optional: size guard (e.g., 2MB)
        max_bytes = 2 * 1024 * 1024
        if f.size > max_bytes:
            raise forms.ValidationError("File too large (max 2MB).")

        return f

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post

    fields = ['title', 'preview', 'read_time', 'content_html_file', 'content', 'tag', 'featured_image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def clean_html_upload(self):
        f = self.cleaned_data.get("content_html_file")
        if not f:
            return None

        name = (f.name or "").lower()
        if not name.endswith((".html", ".htm")):
            raise forms.ValidationError("Please upload an .html or .htm file.")

        # optional: size guard (e.g., 2MB)
        max_bytes = 2 * 1024 * 1024
        if f.size > max_bytes:
            raise forms.ValidationError("File too large (max 2MB).")

        return f

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
