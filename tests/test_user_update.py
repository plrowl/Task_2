import uuid
import requests
import allure
from config import urls, status_codes as sc, messages as msg


@allure.feature("User")
@allure.story("Update user data")
class TestUserUpdate:

    @allure.title("Изменение имени с авторизацией")
    def test_update_user_name_with_auth(self, create_user):
        _, token = create_user
        headers = {"Authorization": token}

        with allure.step("Отправляем PATCH /auth/user с новым именем"):
            resp = requests.patch(
                urls.AUTH_USER_URL,
                headers=headers,
                json={"name": "updated_name"},
            )

        with allure.step("Проверяем ответ"):
            assert resp.status_code == sc.HTTP_OK
            body = resp.json()
            assert body["success"] is True
            assert body["user"]["name"] == "updated_name"

    @allure.title("Изменение email с авторизацией")
    def test_update_user_email_with_auth(self, create_user):
        _, token = create_user
        headers = {"Authorization": token}
        new_email = f"upd_{uuid.uuid4().hex[:6]}@example.com"

        with allure.step("Отправляем PATCH /auth/user с новым email"):
            resp = requests.patch(
                urls.AUTH_USER_URL,
                headers=headers,
                json={"email": new_email},
            )

        assert resp.status_code == sc.HTTP_OK
        assert resp.json()["user"]["email"] == new_email

    @allure.title("Изменение без авторизации (ожидаем 401)")
    def test_update_user_without_auth(self):
        with allure.step("Пробуем изменить профиль без токена"):
            resp = requests.patch(
                urls.AUTH_USER_URL,
                json={"name": "noauth"},
            )

        assert resp.status_code == sc.HTTP_UNAUTHORIZED
        body = resp.json()
        assert body["success"] is False
        assert body["message"] == msg.Messages.UNAUTHORIZED