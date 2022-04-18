from django.urls import path

from . import views

urlpatterns = [
    path("albums/<slug>/analyses/", views.AnalysisListView.as_view()),
    path("albums_analyses/<int:pk>", views.AnalysisDetailsView.as_view()),
    path("albums_analyses/<int:analysis_id>/like", views.LikeAnalysisView.as_view()),
]
