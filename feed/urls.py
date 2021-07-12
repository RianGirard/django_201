from django.urls import path
from django.views.generic.dates import ArchiveIndexView
from . import views 
from feed.models import Post
from feed.views import PostYearArchiveView
from feed.views import PostMonthArchiveView
from feed.views import PostArchiveIndexView

app_name = "feed"
urlpatterns = [
    path("", views.HomePage.as_view(), name="index"),
    path("<int:pk>/", views.PostDetailView.as_view(), name="detail"),
    path("new/", views.CreateNewPost.as_view(), name="new_post"),
    path("archive/", PostArchiveIndexView.as_view(model=Post, date_field="date"), name="archive"),
    path("archive/<int:year>/", PostYearArchiveView.as_view(), name="archive_year"),
    path("archive/<int:year>/<int:month>/", PostMonthArchiveView.as_view(month_format='%m'), name="archive_month_numeric"),
]

