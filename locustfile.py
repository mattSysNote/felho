import random
from locust import HttpUser, task, between

class DjangoAppUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        response = self.client.get("/")
        self.csrftoken = response.cookies.get('csrftoken', '')

    @task(4)
    def view_photo_list(self):
        self.client.get("/", name="Photo List")

    @task(2)
    def view_photo_detail(self):
        photo_id = random.randint(1, 20) 
        with self.client.get(f"/photo/{photo_id}/", name="Photo Detail", catch_response=True) as response:
            if response.status_code == 404:
                response.success()

    @task(1)
    def load_register_page(self):
        self.client.get("/register/", name="Load Register Page")
        
    @task(1)
    def register_user(self):
        headers = {"X-CSRFToken": self.csrftoken}
        payload = {"username": f"user_{random.randint(1, 10000)}", "password": "testpassword123"}
        self.client.post("/register/", data=payload, headers=headers, name="Register User")

    @task(2)
    def login_user(self):
        headers = {"X-CSRFToken": self.csrftoken}
        
        payload = {
            "username": f"user_{random.randint(1, 10000)}", 
            "password": "testpassword123"
        }
        
        self.client.post("/login/", data=payload, headers=headers, name="Login User")