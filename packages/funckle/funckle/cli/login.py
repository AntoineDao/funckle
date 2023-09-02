import random
import webbrowser
import socket
import urllib.parse
import requests
from .settings import settings

HOST = '127.0.0.1'

# Open a browser window to login page: <speckle-server>/authn/verify/<speckle-app-id>/<challenge>
def login_user():
    # Get the challenge from the server
    challenge = (
        str(random.random())[2:15] +
        str(random.random())[2:15]
    )

    print(f"Go to {settings.speckle_server}authn/verify/{settings.speckle_app_id}/{challenge} to login")

    # Open a browser window to the login page
    webbrowser.open(f"{settings.speckle_server}authn/verify/{settings.speckle_app_id}/{challenge}")

    # Start a local server to receive the callback
    # https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, settings.auth_port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            data = conn.recv(1024)
            query = urllib.parse.urlparse(data.decode('utf-8')).query
            access_code = urllib.parse.parse_qs(query)['access_code'][0].split(' ')[0]
            response = b'HTTP/1.1 200 OK\nContent-Type: text/html\n\n<html><body><h1>Login successful</h1></body></html>'
            conn.sendall(response)
        s.close()

    res = requests.post(
        f'{settings.speckle_server}auth/token',
        json={
            'appId': settings.speckle_app_id,
            'appSecret': settings.speckle_app_secret,
            'accessCode': access_code,
            'challenge': challenge
        }
    )

    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Error logging in")
        print(e)
        return

    data = res.json()
    settings.speckle_auth_token = data['token']
    settings.speckle_refresh_token = data['refreshToken']

    settings.persist()

    print("Login successful")