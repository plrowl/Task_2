import uuid
import requests
import allure
from config import urls, data, status_codes as sc, messages as msg


@allure.feature("Auth")
@allure.story("Login")
class TestAuthLogin:

    @allure.title("Успешный логин под существующим пользователем")
    def test_login_existing_user(self):
        email = f"user_{uuid.uuid4().hex[:8]}@example.com"
        with allure.step("Создаём пользователя через /auth/register"):
            reg_resp = requests.post(urls.AUTH_REGISTER_URL, json={
                "email": email,
                "password": data.DEFAULT_PASSWORD,
                "name": "login user",
            })
            assert reg_resp.status_code == sc.HTTP_OK
        with allure.step("Отправляем POST /auth/login с теми же данными"):
            resp = requests.post(urls.AUTH_LOGIN_URL, json={
                "email": email,
                "password": data.DEFAULT_PASSWORD,
            })
        with allure.step("Проверяем, что логин успешен"):
            assert resp.status_code == sc.HTTP_OK
            body = resp.json()
            assert body["success"] is True
            assert "accessToken" in body
            assert "refreshToken" in body
            assert "user" in body

    @allure.title("Логин с неверными данными")
    def test_login_with_wrong_credentials(self):
        with allure.step("Отправляем POST /auth/login с неверными логином и паролем"):
            resp = requests.post(urls.AUTH_LOGIN_URL, json={
                "email": data.INVALID_EMAIL,
                "password": data.INVALID_PASSWORD,
            })

        with allure.step("Проверяем, что сервер вернул 401 и нужное сообщение"):
            assert resp.status_code == sc.HTTP_UNAUTHORIZED
            body = resp.json()
            assert body["success"] is False
            assert body["message"] == msg.Messages.INVALID_CREDENTIALS
