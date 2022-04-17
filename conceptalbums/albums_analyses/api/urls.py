from django.urls import path

from . import views

# router = routers.SimpleRouter()

# router.register(r'albums/', views.AlbumList)
# router.register(r'albums/{slug}/', views.AlbumRetrieve)

urlpatterns = [
    path('albums/<slug>/analyses/', views.AnalysisListView.as_view())
]
