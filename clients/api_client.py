import requests


class APIClient:
    """Client for authenticating and making API requests with token/MFA support."""

    def __init__(self, api_url, username, password, mfa_code):
        """Initialize client with API URL, credentials, and MFA code."""

        self.api_url = api_url
        self.username = username
        self.password = password
        self.mfa_code = mfa_code
        self.token = None

    def authenticate(self):
        """Authenticate user and obtain bearer token via MFA verification."""
        
        # Token 
        r = requests.post(f"{self.api_url}/auth/token", json={"email": self.username, "password": self.password})
        r.raise_for_status()
        token = r.json()["mfa_token"]

        # MFA Verify
        r = requests.post(f"{self.api_url}/auth/mfa/verify", json={"mfa_token": token, "code": self.mfa_code})
        r.raise_for_status()
        self.token = r.json()["access_token"]
 
    
    def put(self, endpoint, payload, token_override="Valid"):        
        """Send PUT request with simulated valid, missing, or invalid bearer token."""

        if token_override == "Missing":
            headers = {}
        elif token_override == "Invalid":
            headers = {"Authorization": "Bearer abc123"}
        else:
            headers = {"Authorization": f"Bearer {self.token}"}

        r = requests.put(f"{self.api_url}{endpoint}", json=payload, headers=headers)
        return r