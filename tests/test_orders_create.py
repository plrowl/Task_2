import requests
import allure
from config import urls, data, status_codes as sc, messages as msg


@allure.feature("Orders")
@allure.story("Create order")
class TestOrdersCreate:


    @allure.title("Создание заказа с авторизацией и валидными ингредиентами")
    def test_create_order_with_auth_and_ingredients(self, auth_headers, ingredients_ids):
        with allure.step("Отправляем POST /orders c токеном и валидными ингредиентами"):
            resp = requests.post(
                urls.ORDERS_URL,
                headers=auth_headers,
                json={"ingredients": ingredients_ids[:2]},
            )

        with allure.step("Проверяем, что заказ создан"):
            assert resp.status_code == sc.HTTP_OK
            body = resp.json()
            assert body["success"] is True
            assert "order" in body

    @allure.title("Создание заказа без авторизации")
        #по доке должен отдать 401(?) поскольку нет авторизации после перенаправления на /login. По факту в постмане отдает 200  {"success": true,"name": "Метеоритный бессмертный бургер","order": {"number": 2609} } поэтому, тест зафолсится. Видимо, недоработка функционала, также пробел в логике API, хорошо бы уточнить у разработки и скорректировать этот шаг.
    def test_create_order_without_auth(self):
        with allure.step("Отправляем POST /orders без токена"):
            resp = requests.post(
                urls.ORDERS_URL,
                json={"ingredients": data.VALID_INGREDIENTS},
            )
        assert resp.status_code == sc.HTTP_UNAUTHORIZED


    @allure.title("Создание заказа с невалидными ингредиентами")
    def test_create_order_with_wrong_ingredients(self, auth_headers):
        with allure.step("Отправляем POST /orders с невалидными id"):
            resp = requests.post(
                urls.ORDERS_URL,
                headers=auth_headers,
                json={"ingredients": data.INVALID_INGREDIENTS},
            )
        assert resp.status_code == sc.HTTP_BAD_REQUEST
        body = resp.json()
        assert body["success"] is False
        assert body["message"] == msg.Messages.INVALID_HASH



    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, auth_headers):
        with allure.step("Отправляем POST /orders с пустым списком ингредиентов"):
            resp = requests.post(
                urls.ORDERS_URL,
                headers=auth_headers,
                json={"ingredients": []},
            )

        with allure.step("Проверяем что сервер вернул 400"):
            assert resp.status_code == sc.HTTP_BAD_REQUEST
            body = resp.json()
            assert body["success"] is False
            assert body["message"] == msg.Messages.EMPTY_INGREDIENTS






        
