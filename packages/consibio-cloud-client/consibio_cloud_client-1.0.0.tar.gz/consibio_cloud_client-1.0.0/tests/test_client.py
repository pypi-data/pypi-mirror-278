from consibio_cloud_client import Client


def test_client_initialization():
    client = Client("http://0.0.0.0")
    assert client.get_api_url() == "http://0.0.0.0"


def test_client_initialization_with_trailing_slash():
    client = Client("http://0.0.0.0/")
    # Test that the trailing slash is removed
    assert client.get_api_url() == "http://0.0.0.0"

# # Test if it's possible to login
# def test_login():
#     client = Client("http://0.0.0.0")
#     assert client.auth_login("testuser", "testpassword") == True
