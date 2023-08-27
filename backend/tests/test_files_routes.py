import pathlib


def test_list_files_returns_registered_files_and_200(client, tmp_path):
    mock_file_1 = tmp_path / "test1.txt"
    mock_file_1.write_text("testtest")

    with open(str(mock_file_1), "rb") as mock_file_stream:
        response = client.post("/files/", files={"file": mock_file_stream})

    mock_file_1_data = response.json()

    mock_file_2 = tmp_path / "test2.txt"
    mock_file_2.write_text("testtest")

    with open(str(mock_file_2), "rb") as mock_file_stream:
        response = client.post("/files/", files={"file": mock_file_stream})

    mock_file_2_data = response.json()

    response = client.get("/files/")

    assert response.status_code == 200
    assert response.json() == [mock_file_1_data, mock_file_2_data]


def test_file_details_returns_specified_file_and_200(client, tmp_path):
    mock_file = tmp_path / "test.txt"
    mock_file.write_text("testtest")

    with open(str(mock_file), "rb") as mock_file_stream:
        response = client.post("/files/", files={"file": mock_file_stream})

    response_data = response.json()
    created_file_id = response_data["id"]

    response = client.get(f"/files/{created_file_id}/")

    assert response.status_code == 200
    assert response.json() == response_data


def test_file_details_returns_404_if_does_not_exist(client):
    non_existent_id = "06f02980-864d-4832-a894-2e9d2543a79a"
    response = client.get(f"/files/{non_existent_id}/")

    assert response.status_code == 404


def test_file_deletion_returns_404_if_does_not_exist(client):
    non_existent_id = "06f02980-864d-4832-a894-2e9d2543a79a"
    response = client.delete(f"/files/{non_existent_id}/")

    assert response.status_code == 404


def test_file_deletion_deletes_record_and_file(client, tmp_path):
    mock_file = tmp_path / "test.txt"
    mock_file.write_text("testtest")

    with open(str(mock_file), "rb") as mock_file_stream:
        response = client.post("/files/", files={"file": mock_file_stream})

    response_data = response.json()
    file_id = response_data["id"]
    file_path = response_data["path"]

    assert pathlib.Path(file_path).exists()
    response = client.get(f"/files/{file_id}/")

    assert response.status_code == 200

    client.delete(f"/files/{file_id}/")
    assert not pathlib.Path(file_path).exists()

    response = client.get(f"/files/{file_id}/")

    assert response.status_code == 404


def test_file_deletion_200_and_return_deleted_resource(client, tmp_path):
    mock_file = tmp_path / "test.txt"
    mock_file.write_text("testtest")

    with open(str(mock_file), "rb") as mock_file_stream:
        response = client.post("/files/", files={"file": mock_file_stream})

    response_data = response.json()
    file_id = response_data["id"]

    response = client.delete(f"/files/{file_id}/")

    assert response.status_code == 200
    assert response.json() == response_data


def test_file_downloads_200_and_return_file(client, tmp_path):
    mock_file = tmp_path / "test.txt"
    mock_file.write_text("testtest")

    with open(str(mock_file), "rb") as mock_file_stream:
        response = client.post("/files/", files={"file": mock_file_stream})

    response_data = response.json()
    file_id = response_data["id"]

    response = client.get(f"/files/{file_id}/content/")

    assert response.status_code == 200
    assert response.text == mock_file.read_text()


def test_file_downloads_404_if_does_not_exist(client):
    non_existent_id = "06f02980-864d-4832-a894-2e9d2543a79a"
    response = client.get(f"/files/{non_existent_id}/content/")

    assert response.status_code == 404