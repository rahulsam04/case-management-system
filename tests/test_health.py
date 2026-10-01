from fastapi import status


def test_health_check(client):
    """Test that the health endpoint returns 200 OK and healthy status."""
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "healthy"}
