import random
from locust import HttpUser, task, between

class DjangoAppUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        """
        This runs when a simulated user starts. 
        We hit the index page to get the initial CSRF token cookie.
        """
        response = self.client.get("/")
        self.csrftoken = response.cookies.get('csrftoken', '')

    @task(4)
    def view_photo_list(self):
        """Task weight 4: Users will hit the index page most often."""
        self.client.get("/", name="Photo List")

    @task(2)
    def view_photo_detail(self):
        """Task weight 2: Randomly view photos (assuming IDs 1-20 exist)."""
        photo_id = random.randint(1, 20) 
        # Catch exceptions in case the ID doesn't exist so it doesn't fail the test
        with self.client.get(f"/photo/{photo_id}/", name="Photo Detail", catch_response=True) as response:
            if response.status_code == 404:
                response.success() # Ignore 404s for the sake of the load test

    @task(1)
    def load_register_page(self):
        """Task weight 1: Check the register page."""
        self.client.get("/register/", name="Load Register Page")
        
    @task(1)
    def register_user(self):
        headers = {"X-CSRFToken": self.csrftoken}
        payload = {"username": f"user_{random.randint(1, 10000)}", "password": "testpassword123"}
        self.client.post("/register/", data=payload, headers=headers, name="Register User")