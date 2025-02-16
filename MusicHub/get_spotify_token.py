import base64
import requests

client_id = 'cddafd384a6b410186c5590513258e54'
client_secret = '67c0e5b8758d4971aded0856298ed853'
auth_str = f"{client_id}:{client_secret}"
b64_auth_str = base64.b64encode(auth_str.encode()).decode()
url = "https://accounts.spotify.com/api/token"
headers = {
    "Authorization": f"Basic {b64_auth_str}"
}
data = {
    "grant_type": "client_credentials"
}

response = requests.post(url, headers=headers, data=data)
token_info = response.json()

if 'access_token' in token_info:
    access_token = token_info['access_token']
    print(f"Access Token: {access_token}")
else:
    print("Error in obtaining access token:", token_info)
