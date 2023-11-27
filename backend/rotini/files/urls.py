import django.urls as dj_urls
import rest_framework.routers as drf_routers

import files.views as file_views

router = drf_routers.DefaultRouter()
router.register("files", file_views.FileViewSet, basename="files")

urlpatterns = router.urls + [
    dj_urls.path(
        "files/<str:file_id>/content/",
        file_views.FileDataView.as_view(),
        name="files-detail-data",
    ),
]
