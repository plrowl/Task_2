import requests
import allure
from config import urls, status_codes as sc, messages as msg, data as test_data


@allure.feature("Orders")
@allure.story("Get user orders")
class TestOrdersGetUser:

    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_orders_authorized_user(self, auth_headers):
        with allure.step("Создаём заказ чтобы вернулся не пустой список"):
            requests.post(
                urls.ORDERS_URL,
                headers=auth_headers,
                json={"ingredients": test_data.VALID_INGREDIENTS},
            )

        with allure.step("Запрашиваем GET /orders c токеном"):
            resp = requests.get(urls.ORDERS_URL, headers=auth_headers)

        with allure.step("Проверяем, что заказы вернулись"):
            assert resp.status_code == sc.HTTP_OK
            body = resp.json()
            assert body["success"] is True
            assert "orders" in body

    @allure.title("Получение заказов без авторизации")
    def test_get_orders_unauthorized_user(self):
        with allure.step("Запрашиваем GET /orders без токена"):
            resp = requests.get(urls.ORDERS_URL)

        assert resp.status_code == sc.HTTP_UNAUTHORIZED
        body = resp.json()
        assert body["success"] is False
        assert body["message"] == msg.Messages.UNAUTHORIZED
