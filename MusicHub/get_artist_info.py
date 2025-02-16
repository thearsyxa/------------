import requests

spotify_artist_id = '0TnOYISbd1XYRBk9myaseg'  
access_token = 'BQD8aXlX0hfpV-Ljl1_r7guIUDelV0D9305rm5i-ky6CGZFH7jPPCwKbU2lwhbUcWniYad57S9lgIdyUrB6yO5PbTKEN90DdxydYz9xe0207n1KhD6dd8Jps1lxZ-wv87fkVQ0Vju-U'  # Вставьте токен доступа


def get_artist_info(spotify_artist_id, access_token):
    url = f"https://api.spotify.com/v1/artists/{spotify_artist_id}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    return response.json()
artist_info = get_artist_info(spotify_artist_id, access_token)
print(artist_info)
