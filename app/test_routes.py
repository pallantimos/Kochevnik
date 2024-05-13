import unittest

from dotenv import dotenv_values
from flask import jsonify
from marshmallow import ValidationError

from app import app
config = dotenv_values(".env")


class TestRegistrationSubmit(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_existing_email(self):
        data = {
            "email": "Adondokov@bk.ru",
            "password": "Validpassword1",
            "name": "Aldar",
            "surname": "Ivanov",
            "phone": "+5555555555",
            "date": "2025-12-12"
        }
        response = self.client.post("/registratesubmit", json=data)
        assert response.status_code == 401
        assert response.json['error'], "Почта зарегистрирована"

    def test_existing_phone(self):
        data = {
            "email": "Adondokov@bk.ru",
            "password": "Validpassword1",
            "name": "Aldar",
            "surname": "Ivanov",
            "phone": "+5555555555",
            "date": "2025-12-12"
        }
        response = self.client.post("/registratesubmit", json=data)
        assert response.status_code == 401
        assert response.json['error'], "Телефон зарегистрирован"

    def test_invalid_date_birth(self):
        data = {
            "email": "Adondokov@bk.ru",
            "password": "Validpassword1",
            "name": "Aldar",
            "surname": "Ivanov",
            "phone": "+5555555555",
            "date": "1820-12-12"
        }
        response = self.client.post("/registratesubmit", json=data)
        assert response.status_code == 401
        assert response.json['error'], "Некорректная дата рождения"

    def test_date_birth_future(self):
        data = {
            "email": "Adondokov@bk.ru",
            "password": "Validpassword1",
            "name": "Aldar",
            "surname": "Ivanov",
            "phone": "+5555555555",
            "date": "2025-12-12"
        }
        response = self.client.post("/registratesubmit", json=data)
        assert response.status_code == 401
        assert response.json['error'], "Некорректная дата рождения"

    def test_main_page(self):
        response = self.client.get('/index')
        assert response.status_code == 200

    def test_invalid_password(self):
        data = {
            "password": "invalidpassword",
            "tel": "+79137591929",
        }
        response = self.client.post("/loginsubmit", json=data)
        assert response.status_code == 401
        assert response.json['error'], "Неправильный пароль"

    def test_login_not_in_database(self):
        data = {
            "password": "Validpassword1",
            "tel": "+79137591930",
        }
        response = self.client.post("/loginsubmit", json=data)
        assert response.status_code == 401
        assert response.json['error'], "Пользователь не найден"

    def test_valid_login(self):
        data = {
            "password": "Cityofdreams5",
            "tel": "+79137591929",
        }
        response = self.client.post("/loginsubmit", json=data)
        assert response.status_code == 200

    def test_valid_registration(self):
        data = {
            "email": "Test@bk.ru",
            "password": "Cityofdreams5",
            "name": "Aldar",
            "surname": "Ivanov",
            "phone": "+79137591929",
            "date": "2019-11-11"
        }
        response = self.client.post("/registratesubmit", json=data)
        assert response.status_code == 200

    def test_invalid_email(self):
        data = {
            "email": "Adondokovbk.ru",
            "password": "Validpassword1",
            "name": "Aldar",
            "surname": "Ivanov",
            "phone": "+5555555555",
            "date": "2019-11-11"
        }
        response = self.client.post("/registratesubmit", json=data)
        assert response.status_code == 401
        assert response.json['error'], "Неправильный формат почты"

    def test_password_small_length(self):
        data = {
            "email": "Adondokovbk.ru",
            "password": "invalid5",
            "name": "Aldar",
            "surname": "Ivanov",
            "phone": "+5555555555",
            "date": "2019-11-11"
        }
        response = self.client.post("/registratesubmit", json=data)
        assert response.status_code == 401
        assert response.json['error'], "Пароль должен быть длинее 8 символов"

    def test_password__no_uppercase(self):
        data = {
            "email": "Adondokovbk.ru",
            "password": "invalidpassword5",
            "name": "Aldar",
            "surname": "Ivanov",
            "phone": "+5555555555",
            "date": "2019-11-11"
        }
        response = self.client.post("/registratesubmit", json=data)
        assert response.status_code == 401
        assert response.json['error'], "Пароль должен содержать заглавные буквы"

    def test_password_no_lowercase(self):
        data = {
            "email": "Adondokovbk.ru",
            "password": "INVALIDPASSWORD5",
            "name": "Aldar",
            "surname": "Ivanov",
            "phone": "+5555555555",
            "date": "2019-11-11"
        }
        response = self.client.post("/registratesubmit", json=data)
        assert response.status_code == 401
        assert response.json['error'], "Пароль должен содержать строчные буквы"

    def test_password_no_digit(self):
        data = {
            "email": "Adondokovbk.ru",
            "password": "Invalidpassword",
            "name": "Aldar",
            "surname": "Ivanov",
            "phone": "+5555555555",
            "date": "2019-11-11"
        }
        response = self.client.post("/registratesubmit", json=data)
        assert response.status_code == 401
        assert response.json['error'], "Пароль должен содержать цифру"

    def test_password_with_non_alphanumeric(self):
        data = {
            "email": "Adondokovbk.ru",
            "password": "Invalidpassword1!",
            "name": "Aldar",
            "surname": "Ivanov",
            "phone": "+5555555555",
            "date": "2019-11-11"
        }
        response = self.client.post("/registratesubmit", json=data)
        assert response.status_code == 401
        assert response.json['error'], "Пароль должен содержать только английские буквы и цифры"

    def test_duplicate_email(self):
        ...

    def test_validation_error(self):
        ...


if __name__ == "__main__":
    unittest.main()