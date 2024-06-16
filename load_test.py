import random
import string

from locust import HttpUser, task, between


class User:
    def __init__(self):
        self.email = self.generate_random_email()
        self.phone = self.generate_random_phone_number()
        self.name = "Aldar"
        self.surname = "Dondokov"
        self.password = "Cityofdreams5"
        self.date = "1999-12-12"

    def generate_random_email(self):
        # Генерация случайного email
        prefix = ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
        suffix = '@example.com'
        return prefix + suffix

    def generate_random_phone_number(self):
        # Генерация случайного номера в формате 7XXXXXXXXXX
        prefix = '7'
        suffix = ''.join(random.choice(string.digits) for _ in range(9))
        return prefix + suffix


class WebsiteUser(HttpUser):
    wait_time = between(5, 10)

    @task
    def index(self):
        self.client.get("/")

    @task
    def menu(self):
        self.client.get("/menu")

    @task
    def hotels(self):
        self.client.get("/hotels")

    @task
    def login(self):
        self.client.get("/login")

    @task
    def register(self):
        self.client.get("/registrate")
        user = User()

        data = {
            "email": user.email,
            "password": user.password,
            "name": user.name,
            "surname": user.surname,
            "phone": user.phone,
            "date": user.date
        }

        response = self.client.post("registratesubmit", json=data)
        assert response.status_code == 200