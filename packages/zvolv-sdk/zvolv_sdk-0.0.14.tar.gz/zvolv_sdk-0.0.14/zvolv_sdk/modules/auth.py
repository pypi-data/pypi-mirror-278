import requests
import hashlib

class Auth:
    def __init__(self, session, base_url, workspace_instance):
        self.session = session
        self.base_url = base_url
        self.workspace_instance = workspace_instance
        self.user_instance = None

    def login(self, email, password):
        """Authenticate a user and store their auth token."""
        if not email or not password:
            raise ValueError("Email and Password are required to login")
        
        url = f"{self.base_url}/rest/v17/user/login"
        headers = {
            'Content-Type': 'application/json',
            'jwt': 'true',
            'businessDomain': self.workspace_instance['BUSINESS_DOMAIN'],
            'businessTagId': self.workspace_instance['BUSINESS_TAG_ID'],
        }
        sha512pwd = hashlib.sha512(password.encode('utf-8')).hexdigest()
        data = {'email': email, 'password': sha512pwd}
        response = self.session.post(url, json=data, headers=headers)
        if response.status_code == 200:
            resp = response.json()
            if resp.get('error') == False:
                token = resp['loginToken']
                self.session.headers.update({'Authorization': f"Bearer {token}"})
                self.user_instance = resp
            else:
                print("Login Failed")
                print(response.json())

        return response.json()