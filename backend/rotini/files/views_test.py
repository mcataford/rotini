import pathlib

import rest_framework.status as drf_status
import django.urls as django_urls
import pytest

pytestmark = [pytest.mark.anyio, pytest.mark.django_db]


@pytest.mark.parametrize(
    "route_name,route_params",
    [
        ("files-detail-data", {"file_id": "abc"}),
        ("files-list", None),
        ("files-detail", {"pk": "abc"}),
    ],
    ids=["details-data", "list", "details"],
)
def test_files_views_return_401_if_unauthenticated(
    no_auth_client, route_name, route_params
):
    """The files API requires authentication."""
    response = no_auth_client.get(django_urls.reverse(route_name, kwargs=route_params))
    assert response.status_code == drf_status.HTTP_401_UNAUTHORIZED


def test_file_downloads_404_if_does_not_exist(auth_client):
    """Attempting to download a file that doesn't exist yields 404 for authenticated users."""
    non_existent_id = "06f02980-864d-4832-a894-2e9d2543a79a"
    response = auth_client.get(
        django_urls.reverse("files-detail-data", kwargs={"file_id": non_existent_id})
    )

    assert response.status_code == drf_status.HTTP_404_NOT_FOUND


def test_file_deletion_returns_404_if_does_not_exist(auth_client):
    non_existent_id = "06f02980-864d-4832-a894-2e9d2543a79a"
    response = auth_client.delete(
        django_urls.reverse("files-detail", kwargs={"pk": non_existent_id})
    )

    assert response.status_code == drf_status.HTTP_404_NOT_FOUND


def test_file_detail_returns_404_if_does_not_exist(auth_client):
    non_existent_id = "06f02980-864d-4832-a894-2e9d2543a79a"
    response = auth_client.get(
        django_urls.reverse("files-detail", kwargs={"pk": non_existent_id})
    )

    assert response.status_code == drf_status.HTTP_404_NOT_FOUND


def test_list_files_returns_registered_files_and_200(auth_client, tmp_path):
    mock_file_1 = tmp_path / "test1.txt"
    mock_file_1.write_text("testtest")

    with open(str(mock_file_1), "rb") as mock_file_stream:
        response = auth_client.post(
            django_urls.reverse("files-list"), {"file": mock_file_stream}
        )

    mock_file_1_data = response.json()

    mock_file_2 = tmp_path / "test2.txt"
    mock_file_2.write_text("testtest")

    with open(str(mock_file_2), "rb") as mock_file_stream:
        response = auth_client.post(
            django_urls.reverse("files-list"), {"file": mock_file_stream}
        )

    mock_file_2_data = response.json()

    response = auth_client.get("/files/")

    assert response.status_code == drf_status.HTTP_200_OK
    assert response.json() == [mock_file_1_data, mock_file_2_data]


def test_file_details_returns_specified_file_and_200(auth_client, tmp_path):
    mock_file = tmp_path / "test.txt"
    mock_file.write_text("testtest")

    with open(str(mock_file), "rb") as mock_file_stream:
        response = auth_client.post(
            django_urls.reverse("files-list"), {"file": mock_file_stream}
        )

    response_data = response.json()
    created_file_id = response_data["id"]

    response = auth_client.get(
        django_urls.reverse("files-detail", kwargs={"pk": created_file_id})
    )

    assert response.status_code == drf_status.HTTP_200_OK
    assert response.json() == response_data


def test_file_deletion_deletes_record_and_file(auth_client, tmp_path):
    mock_file = tmp_path / "test.txt"
    mock_file.write_text("testtest")

    with open(str(mock_file), "rb") as mock_file_stream:
        response = auth_client.post(
            django_urls.reverse("files-list"), {"file": mock_file_stream}
        )

    response_data = response.json()
    file_id = response_data["id"]
    file_path = response_data["path"]

    assert pathlib.Path(file_path).exists()
    response = auth_client.get(
        django_urls.reverse("files-detail", kwargs={"pk": file_id})
    )

    assert response.status_code == drf_status.HTTP_200_OK

    auth_client.delete(django_urls.reverse("files-detail", kwargs={"pk": file_id}))
    assert not pathlib.Path(file_path).exists()

    response = auth_client.get(
        django_urls.reverse("files-detail", kwargs={"pk": file_id})
    )

    assert response.status_code == drf_status.HTTP_404_NOT_FOUND


def test_file_deletion_200_and_return_deleted_resource(auth_client, tmp_path):
    mock_file = tmp_path / "test.txt"
    mock_file.write_text("testtest")

    with open(str(mock_file), "rb") as mock_file_stream:
        response = auth_client.post(
            django_urls.reverse("files-list"), {"file": mock_file_stream}
        )

    response_data = response.json()
    file_id = response_data["id"]

    response = auth_client.delete(
        django_urls.reverse("files-detail", kwargs={"pk": file_id})
    )

    assert response.status_code == drf_status.HTTP_204_NO_CONTENT


def test_file_downloads_200_and_return_file(auth_client, tmp_path):
    mock_file = tmp_path / "test.txt"
    mock_file.write_text("testtest")

    with open(str(mock_file), "rb") as mock_file_stream:
        response = auth_client.post(
            django_urls.reverse("files-list"), {"file": mock_file_stream}
        )

    response_data = response.json()
    file_id = response_data["id"]

    response = auth_client.get(
        django_urls.reverse("files-detail-data", kwargs={"file_id": file_id})
    )

    assert response.status_code == drf_status.HTTP_200_OK
    assert response.content.decode("utf8") == mock_file.read_text()
