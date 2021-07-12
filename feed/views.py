from typing import Text
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.dates import ArchiveIndexView
from django.views.generic.dates import YearArchiveView
from django.views.generic.dates import MonthArchiveView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from followers.models import Follower
from .models import Post 

class HomePage(TemplateView):
    http_method_names = ['get']
    template_name = "feed/homepage.html"
    model = Post

    def dispatch(self, request, *args, **kwargs):                   # this method here... 
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if self.request.user.is_authenticated:                      # allows us to reference self.request.user ... 
            following = list(
                Follower.objects.filter(followed_by=self.request.user).values_list('following', flat=True)
            )
            if not following:
                # if user is not following anyone, show the default 30 posts most recently made by all
                posts = Post.objects.all().order_by('-id')[0:30]
            else:
                posts = Post.objects.filter(author__in=following).order_by('-id')[0:60]
        else: 
            posts = Post.objects.all().order_by('-id')[0:30]
        context['posts'] = posts
        return context


class PostDetailView(DetailView):
    http_method_names = ['get']
    template_name = "feed/detail.html"
    model = Post
    context_object_name = "post"

class CreateNewPost(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "feed/create.html"
    fields = ['text']
    success_url = "/"

    def dispatch(self, request, *args, **kwargs):           # dispatch is required to give self.request a value, so that it can be assigned below as "author"
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        post = Post.objects.create(
            text=request.POST.get("text"),
            author=request.user,
        )
        return render(
            request,
            "includes/post.html",
            {
                "post": post,
                "show_detail_link": True,
            },
            content_type="application/html"
        )

class PostArchiveIndexView(ArchiveIndexView):
    date_list_period = "month"

class PostYearArchiveView(YearArchiveView):
    queryset = Post.objects.all()
    date_field = "date"
    make_object_list = True
    allow_future = True

class PostMonthArchiveView(MonthArchiveView):
    queryset = Post.objects.all()
    date_field = "date"
    # make_object_list = True
    allow_future = True


# Create your views here.
