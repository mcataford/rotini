import pathlib

import django.http as django_http
import django.conf as django_conf
import rest_framework.viewsets as drf_viewsets
import rest_framework.status as drf_status
import rest_framework.views as drf_views
from rest_framework.permissions import IsAuthenticated

import files.serializers as files_serializers
import files.models as files_models


class FileViewSet(drf_viewsets.ModelViewSet):
    """
    File retrieval and manipulation

    GET /file/

    200 OK { [FileSerializerData] }

    On success, returns all the files owned by the logged-in
    user.

    GET /file/{file_id}/

    200 OK { FileSerializerData }

    On success, returns a single file's metadata by ID. Note that
    this does not provide the file data, which can be fetched via
    /file/{file_id}/content/.

    DELETE /file/{file_id}/

    204 NO CONTENT {}

    Deletes an owned file.

    PUT /file/{file_id}/ { FileMetadata }

    200 OK {}

    Mutates the file metadata for the given file. The underlying
    resource on disk stays the same.
    """

    queryset = files_models.File.objects.all()
    serializer_class = files_serializers.FileSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(owner_id=self.request.user.id)

    def create(
        self, request: django_http.HttpRequest, *args, **kwargs
    ) -> django_http.JsonResponse:
        """
        Handles the upload and metadata records for a new file.
        """
        file_received = request.FILES.get("file")

        if not file_received:
            return django_http.HttpResponseBadRequest()

        content = request.FILES.get("file").read()
        size = len(content)
        dest_path = pathlib.Path(
            django_conf.settings.USER_UPLOAD_ROOT, request.FILES.get("file").name
        )

        file = self.get_serializer_class()(
            data={"path": str(dest_path), "size": size, "owner": request.user.id}
        )

        with open(dest_path, "wb") as f:
            f.write(content)

        if file.is_valid(raise_exception=True):
            file.save()

        return django_http.JsonResponse(file.data, status=drf_status.HTTP_201_CREATED)

    def destroy(
        self, request: django_http.HttpRequest, *args, **kwargs
    ) -> django_http.HttpResponse:
        pk = kwargs["pk"]
        file_selected = self.queryset.filter(pk=pk).first()

        if file_selected is None:
            return django_http.HttpResponseNotFound()

        pathlib.Path(file_selected.path).unlink()

        file_selected.delete()

        return django_http.HttpResponse(status=drf_status.HTTP_204_NO_CONTENT)


class FileDataView(drf_views.APIView):
    """File downloads"""

    permission_classes = [IsAuthenticated]

    queryset = files_models.File.objects.all()

    def get_queryset(self):
        return self.queryset.filter(owner_id=self.request.user.id)

    def get(self, _, file_id: str) -> django_http.HttpResponse:
        """
        Retrieves and serves the given file, by ID.

        The file must be owned by the logged-in user, else 404.
        """

        file = self.get_queryset().filter(id=file_id).first()

        if file is None:
            return django_http.HttpResponseNotFound()

        with open(
            pathlib.Path(django_conf.settings.USER_UPLOAD_ROOT, file.path), "rb"
        ) as f:
            return django_http.HttpResponse(
                f.read(),
                headers={"Content-Disposition": f'attachment; filename="{file.path}"'},
                content_type="application/octet-stream",
            )
