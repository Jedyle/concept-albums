from django.urls import path

from . import views

urlpatterns = [
    path("albums/", views.AlbumList.as_view()),
    path("albums/<slug>/", views.AlbumRetrieve.as_view()),
]
