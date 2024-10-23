from typing import List
import requests
import json
import base64

def create_x_csrf_token_header(session):
    # Get the cookies from the session
    cookies = session.cookies.get_dict()
    
    if 'TOKEN' in cookies:
        jwt = cookies['TOKEN']

        jwt_components = jwt.split('.')
        
        if len(jwt_components) < 2:
            return

        # Remove any existing x-csrf-token headers first
        session.headers.pop('x-csrf-token', None)

        # Decode the JWT payload and extract csrfToken
        payload = base64.urlsafe_b64decode(jwt_components[1] + '==')  # Padding for base64
        csrf_token = json.loads(payload).get('csrfToken')

        if csrf_token:
            session.headers['x-csrf-token'] = csrf_token

# Replace with your UniFi credentials and base URL
username = 'api_tester'
password = 'Test_Password12'
baseurl = 'https://10.0.0.1'
site = 'default'

# Create a session object to persist cookies
session = requests.Session()

# Set up session options to ignore SSL warnings
session.verify = False  # Use this with caution; it ignores SSL certificate validation

# Login data payload
login_data = {
    "username": username,
    "password": password
}

# Attempt to log in to the UniFi controller
login_response = session.post(f'{baseurl}/api/auth/login', json=login_data)

# Check if login was successful
if login_response.ok:
    print("Login successful!")
else:
    print("Login failed!")
    print("Response:", login_response.text)

# You can now make additional requests using the session
# For example, to get the user's data:
response = session.get(f'{baseurl}/api/users/self')

create_x_csrf_token_header(session)

if response.ok:
    devices = response.json()
    print("Self:", json.dumps(devices, indent=4))
else:
    print("Failed to retrieve self!")
    print("Response:", response.text)

# Optionally, log out when done
logout_response = session.post(f'{baseurl}/api/auth/logout')
print(logout_response.text)
if logout_response.ok:
    print("Logged out successfully!")
else:
    print("Failed to log out!")
