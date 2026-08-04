def test_get_deliveries(client):

    response = client.get(
        "/deliveries"
    )

    assert response.status_code in [200,401]