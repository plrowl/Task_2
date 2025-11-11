import uuid
import pytest
import requests
import allure
from config import urls, data


def _make_unique_user():
    uniq = uuid.uuid4().hex[:8]
    return {
        "email": f"autotest_{uniq}@example.com",
        "password": data.DEFAULT_PASSWORD,
        "name": f"autotest_{uniq}",
    }


@pytest.fixture
def create_user():
    with allure.step("Создаём тестового пользователя через /auth/register"):
        user_data = _make_unique_user()
        resp = requests.post(urls.AUTH_REGISTER_URL, json=user_data)
        resp.raise_for_status()
        token = resp.json().get("accessToken")

    yield user_data, token

    with allure.step("Удаляем тестового пользователя через /auth/user"):
        if token:
            headers = {"Authorization": token}
            requests.delete(urls.AUTH_USER_URL, headers=headers)


@pytest.fixture
def auth_headers(create_user):
    _, token = create_user
    return {"Authorization": token}


@pytest.fixture
def ingredients_ids():
    response = requests.get(urls.INGREDIENTS_URL)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    return [ingredient["_id"] for ingredient in data["data"][:2]]


@pytest.fixture
def create_order(auth_headers, ingredients_ids):
    with allure.step("Создаём заказ для авторизованного пользователя"):
        resp = requests.post(
            urls.ORDERS_URL,
            headers=auth_headers,
            json={"ingredients": ingredients_ids},
        )
        resp.raise_for_status()
        order_body = resp.json()
    yield order_body
