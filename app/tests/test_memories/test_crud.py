from httpx import AsyncClient
from starlette import status

from app.main import app


async def test_crud_memory(
        client: AsyncClient,
        default_user_headers: dict[str, str],
) -> None:
    response = await client.post(
        app.url_path_for("post_memory"),
        headers=default_user_headers,
        json={
            "header": "test",
            "text": "test",
            "photos": [
                "https://test.com/",
                "https://test2.com",
            ]
        }
    )
    assert response.status_code == status.HTTP_200_OK
    response = await client.get(
        app.url_path_for("get_memories"),
        headers=default_user_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    memory_id = int(response.json()[0]['id'])
    photo_id = int(response.json()[0]['photos'][0]['id'])
    response = await client.get(
        app.url_path_for('get_memory', memory_id=memory_id),
        headers=default_user_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    response = await client.put(
        app.url_path_for("update_memory"),
        headers=default_user_headers,
        json={
            "id": memory_id,
            "header": "test_update",
            "text": "test_updated",
            "photos": [
                {
                    "id": photo_id,
                    "photo_url": "https://example_update.com/"
                }
            ]
        }
    )
    assert response.status_code == status.HTTP_200_OK

    response = await client.delete(
        app.url_path_for("delete_memory", memory_id=memory_id),
        headers=default_user_headers)
    assert response.status_code == status.HTTP_200_OK

    response = await client.get(
        app.url_path_for("get_other_memories"),
        headers=default_user_headers,
    )
    assert response.status_code == status.HTTP_200_OK
