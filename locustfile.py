from locust import HttpUser, task, between
import uuid
import random

class DjangoAppUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        # Fetch initial CSRF token
        response = self.client.get("/")
        self.csrftoken = response.cookies.get('csrftoken', '')
        
        # Initialize default credentials so tasks don't crash if called out of order
        self.username = f"user_{uuid.uuid4().hex[:8]}"
        self.password = "Testpassword123??"

    @task(4)
    def view_photo_list(self):
        self.client.get("/", name="Photo List")

    @task(2)
    def view_photo_detail(self):
        photo_id = random.randint(1, 20) 
        with self.client.get(f"/photo/{photo_id}/", name="Photo Detail", catch_response=True) as response:
            if response.status_code in [200, 404]:
                response.success()

    @task(1)
    def load_register_page(self):
        self.client.get("/register/", name="Load Register Page")
        
    @task(3)
    def register_user(self):
        self.client.cookies.clear()
        
        response = self.client.get("/register/")
        csrftoken = response.cookies.get("csrftoken", "")

        new_username = f"user_{uuid.uuid4().hex[:8]}"

        payload = {
            "username": new_username,
            "password1": self.password, 
            "password2": self.password, 
            "csrfmiddlewaretoken": csrftoken
        }
        
        headers = {
            "X-CSRFToken": csrftoken
        }

        with self.client.post("/register/", data=payload, headers=headers, catch_response=True, allow_redirects=False, name="Register User") as response:
            if response.status_code == 302:
                response.success()
                self.username = new_username
            else:
                print(f"--- REGISTRATION FAILED --- Status: {response.status_code}")
                print(response.text) 
                response.failure(f"Registration failed! HTTP {response.status_code}.")

    @task(1)
    def login_user(self):
        self.client.cookies.clear()
        
        response = self.client.get("/accounts/login/")
        csrftoken = response.cookies.get("csrftoken", "")

        payload = {
            "username": self.username, 
            "password": self.password,
            "csrfmiddlewaretoken": csrftoken
        }
        
        headers = {
            "X-CSRFToken": csrftoken
        }
        
        with self.client.post("/login/", data=payload, headers=headers, catch_response=True, allow_redirects=False, name="Login User") as response:
            if response.status_code == 302:
                response.success()
            else:
                print(f"--- LOGIN FAILED --- Status: {response.status_code}")
                print(response.text) 
                response.failure(f"Login failed! HTTP {response.status_code}.")