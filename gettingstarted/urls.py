from django.urls import path, include

from django.contrib import admin

admin.autodiscover()

import hello.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", hello.views.index, name="index"),
    path("index_with_textbox/", hello.views.index, name="index_with_textbox"),
    path("db/", hello.views.db, name="db"),
    path("admin/", admin.site.urls),
    path("calculatesimilarity/", hello.views.calculatesimilarity, name="calculatesimilarity"),
    path("calculatesimilarity/download_csv_label/", hello.views.download_csv_label, name="download_csv_label"),
    path("calculatesimilarity/download_csv_val/", hello.views.download_csv_val, name="download_csv_val")
]
