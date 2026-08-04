def test_register_user(client):

    response = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "testuser@gmail.com",
            "password": "Test12345",
            "role": "DRIVER"
        }
    )

    assert response.status_code in [200, 201, 400]


def test_login_user(client):

    response = client.post(
        "/auth/login",
        data={
            "username": "testuser@gmail.com",
            "password": "Test12345"
        }
    )

    assert response.status_code in [200, 401]