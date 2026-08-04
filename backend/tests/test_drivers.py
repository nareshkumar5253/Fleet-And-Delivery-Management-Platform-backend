def test_get_drivers(client):

    response = client.get(
        "/drivers"
    )

    assert response.status_code in [200,401]