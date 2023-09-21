
from django.urls import path

from home.views import BlogView,PublicBlogView

urlpatterns = [

    path('blog/', BlogView.as_view()),
    path('', PublicBlogView.as_view()),
]
