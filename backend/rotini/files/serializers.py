import typing
import pathlib

import rest_framework.serializers as drf_serializers

import files.models as files_models


class FileDict(typing.TypedDict):
    id: str
    path: str
    size: int
    filename: str
    owner_id: int


class FileSerializer(drf_serializers.ModelSerializer):
    def validate_path(self, value: str) -> typing.Union[typing.NoReturn, str]:
        if not value:
            raise drf_serializers.ValidationError("Path must not be empty.")
        return value

    def validate_owner(self, value: int) -> typing.Union[typing.NoReturn, int]:
        if not value:
            raise drf_serializers.ValidationError("File must have an owner.")
        return value

    def to_representation(self, instance: files_models.File) -> FileDict:
        return {
            "id": instance.id,
            "path": instance.path,
            "size": instance.size,
            "owner_id": instance.owner.id,
            "filename": pathlib.Path(instance.path).name,
        }

    class Meta:
        model = files_models.File
        fields = "__all__"
