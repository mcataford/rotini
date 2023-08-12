from rotini.use_cases import files as files_use_cases


def test_list_files_returns_registered_files_and_200(client):
    file_1 = files_use_cases.create_file_record("/test1.txt", 123)
    file_2 = files_use_cases.create_file_record("/test2.txt", 456)

    response = client.get("/files/")

    assert response.status_code == 200
    assert response.json() == [file_1, file_2]


def test_file_details_returns_specified_file_and_200(client):
    file = files_use_cases.create_file_record("/test1.txt", 123)

    response = client.get(f"/files/{file['id']}/")

    assert response.status_code == 200
    assert response.json() == file


def test_file_details_returns_404_if_does_not_exist(client):
    non_existent_id = "06f02980-864d-4832-a894-2e9d2543a79a"
    response = client.get(f"/files/{non_existent_id}/")

    assert response.status_code == 404
