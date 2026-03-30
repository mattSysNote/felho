import re

from locust import HttpUser, task, between
import uuid
import random
from PIL import Image
import io
import os

class DjangoAppUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        # Fetch initial CSRF token
        response = self.client.get("/")
        self.csrftoken = response.cookies.get('csrftoken', '')
        
        self.username = f"user_{uuid.uuid4().hex[:8]}"
        self.password = "Testpassword123??"
        self.logged_in = False
        self.registered = False
        self.uploaded_photo_list = []

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
            "X-CSRFToken": csrftoken,
            "Referer": f"{self.client.base_url}/register/" # Spoof the referer
        }

        with self.client.post("/register/", data=payload, headers=headers, catch_response=True, allow_redirects=False, name="Register User") as response:
            if response.status_code == 302:
                response.success()
                self.username = new_username
                self.logged_in = True
                self.registered = True
            else:
                print(f"--- REGISTRATION FAILED --- Status: {response.status_code}")
                print(response.text) 
                response.failure(f"Registration failed! HTTP {response.status_code}.")

    @task(1)
    def login_user(self):
        if not getattr(self, 'registered', False):
            return  
        self.client.cookies.clear()
        
        response = self.client.get("/accounts/login/")
        csrftoken = response.cookies.get("csrftoken", "")

        payload = {
            "username": self.username, 
            "password": self.password,
            "csrfmiddlewaretoken": csrftoken
        }
        
        headers = {
            "X-CSRFToken": csrftoken,
            "Referer": f"{self.client.base_url}/accounts/login/"
        }
        
        with self.client.post("/accounts/login/", data=payload, headers=headers, catch_response=True, allow_redirects=False, name="Login User") as response:
            if response.status_code in [200, 302]:
                response.success()
                self.logged_in = True
            # else:
            #     print(f"--- LOGIN FAILED --- Status: {response.status_code}")
            #     print(response.text) 
            #     response.failure(f"Login failed! HTTP {response.status_code}.")


    @task(2)
    def upload_photo(self):
        if not getattr(self, 'logged_in', False):
            return  
        
        width, height = 250, 250
        block_size = 10 
        small_w, small_h = width // block_size, height // block_size
        random_bytes = os.urandom(small_w * small_h * 3)
        img_small = Image.frombytes('RGB', (small_w, small_h), random_bytes)
        img = img_small.resize((width, height), resample=Image.NEAREST)
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)

        response = self.client.get("/upload/", name="Load Upload Page")
        csrftoken = response.cookies.get("csrftoken", "")

        files = {
            'image': ('test_image.jpg', img_bytes, 'image/jpeg')
        }
        data = {
            "csrfmiddlewaretoken": csrftoken,
            "title": f"Photo {uuid.uuid4().hex[:12]}"
        }
        headers = {
            "X-CSRFToken": csrftoken,
            "Referer": f"{self.client.base_url}/upload/"
        }

        with self.client.post("/upload/", data=data, files=files, headers=headers, catch_response=True, allow_redirects=False, name="Upload Photo") as response:
            if response.status_code == 302:
                response.success()
                redirect_url = response.headers.get('Location', '')
                match = re.search(r'/(\d+)/', redirect_url)
                if match:
                    new_photo_id = match.group(1)
                    if not hasattr(self, 'uploaded_photo_list'):
                        self.uploaded_photo_list = []
                    self.uploaded_photo_list.append(new_photo_id)
            # else:
            #     print(f"--- UPLOAD FAILED --- Status: {response.status_code}")
            #     response.failure(f"Upload failed! HTTP {response.status_code}.")

    @task(1)
    def delete_photo(self):
        if not getattr(self, 'logged_in', False):
            return
        
        response = self.client.get("/", name="Load Photo List for Delete")
        csrftoken = response.cookies.get("csrftoken", "")

        photo_ids = getattr(self, 'uploaded_photo_list', [])
        if not photo_ids:
            return
        random_index = random.randrange(len(photo_ids))
        photo_id_to_delete = photo_ids.pop(random_index)

        data = {
            "csrfmiddlewaretoken": csrftoken
        }
        headers = {
            "X-CSRFToken": csrftoken,
            "Referer": f"{self.client.base_url}/delete/{photo_id_to_delete}/" 
        }

        with self.client.post(f"/delete/{photo_id_to_delete}/", data=data, headers=headers, catch_response=True, allow_redirects=False, name="Delete Photo") as response:
            
            if response.status_code == 302:
                response.success()
            elif response.status_code == 404:
                response.success() 
            else:
                response.failure(f"Delete failed! HTTP {response.status_code}.")


    @task(1)
    def logout_user(self):
        if not getattr(self, 'logged_in', False):
            return
        
        response = self.client.get("/", name="Load Home for Logout")
        csrftoken = response.cookies.get("csrftoken", "")

        headers = {
            "X-CSRFToken": csrftoken,
            "Referer": f"{self.client.base_url}/"
        }

        with self.client.post("/accounts/logout/", data={"csrfmiddlewaretoken": csrftoken}, headers=headers, catch_response=True, name="Logout User") as response:
            
            if response.status_code in [200, 302]:
                response.success()
                self.logged_in = False
                self.registered = False
                self.client.cookies.clear()
            else:
                response.failure(f"Logout failed with status {response.status_code}")