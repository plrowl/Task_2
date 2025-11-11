import uuid
import pytest
import requests
import allure
from config import urls, data, status_codes as sc, messages as msg


@allure.feature("Auth")
@allure.story("Register")
class TestAuthRegister:

    @allure.title("Создание уникального пользователя")
    def test_create_unique_user_success(self):
        with allure.step("Готовим тело запроса"):
            payload = {
                "email": f"user_{uuid.uuid4().hex[:8]}@example.com",
                "password": data.DEFAULT_PASSWORD,
                "name": "new user",
            }

        with allure.step("Отправляем POST /auth/register"):
            resp = requests.post(urls.AUTH_REGISTER_URL, json=payload)

        with allure.step("Проверяем успешный ответ"):
            assert resp.status_code == sc.HTTP_OK
            body = resp.json()
            assert body["success"] is True
            assert "accessToken" in body
            assert "user" in body


    @allure.title("Регистрация уже существующего пользователя")
    def test_create_user_already_registered(self):
        payload = {
            "email": f"user_{uuid.uuid4().hex[:8]}@example.com",
            "password": data.DEFAULT_PASSWORD,
            "name": "test user",
        }

        with allure.step("Первый раз регистрируем пользователя"):
            first = requests.post(urls.AUTH_REGISTER_URL, json=payload)
            assert first.status_code == sc.HTTP_OK

        with allure.step("Повторяем попытку регистрации пользователя"):
            second = requests.post(urls.AUTH_REGISTER_URL, json=payload)

        with allure.step("Проверяем, что вернулась ошибка 403"):
            assert second.status_code == sc.HTTP_FORBIDDEN
            body = second.json()
            assert body["success"] is False
            assert body["message"] == msg.Messages.USER_ALREADY_EXISTS


    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    @allure.title("Регистрация без обязательного поля: {missing_field}")
    def test_create_user_without_required_field(self, missing_field):
        payload = {
            "email": f"user_{uuid.uuid4().hex[:8]}@example.com",
            "password": data.DEFAULT_PASSWORD,
            "name": "no field",
        }
        payload.pop(missing_field)

        with allure.step(f"Отправляем запрос без поля {missing_field}"):
            resp = requests.post(urls.AUTH_REGISTER_URL, json=payload)

        with allure.step("Проверяем, что сервер вернул 403 и success=false"):
            assert resp.status_code == sc.HTTP_FORBIDDEN
            body = resp.json()
            assert body["success"] is False
            assert body["message"] == msg.Messages.MISSING_FIELD