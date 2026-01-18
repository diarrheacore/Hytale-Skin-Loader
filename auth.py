CLIENT_ID = "hytale-launcher"
USER_AGENT = "HytaleSkinLoader/1.0"

AUTH_URL = "https://oauth.accounts.hytale.com/oauth2/auth"
TOKEN_URL = "https://oauth.accounts.hytale.com/oauth2/token"
ACCOUNT_URL = "https://account-data.hytale.com/my-account"
SESSION_URL = "https://sessions.hytale.com/game-session/new"

import requests, json, os
import secrets, hashlib, base64

from authlib.integrations.requests_client import OAuth2Session
from urllib.parse import urlparse, parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler

if os.path.exists("savedauth.json"):
    with open("savedauth.json", "r") as f:
        saved_auth = json.load(f)
        f.close()

client = OAuth2Session(
    client_id=CLIENT_ID,
    client_secret=None,
    redirect_uri="https://accounts.hytale.com/consent/client"
)

sess = requests.Session()
sess.headers.update({"User-Agent": USER_AGENT})

def generate_pkce():
    code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')

    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode('utf-8')).digest()
    ).decode('utf-8').rstrip('=')
    
    return code_verifier, code_challenge

class CallbackHandler(BaseHTTPRequestHandler):
    auth_code = None
    
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        CallbackHandler.auth_code = query.get('code', [None])[0]
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Authorization successful! You can close this window.")

def get_token():
    if os.path.exists("savedauth.json"):
        with open("savedauth.json", "r") as f:
            saved_auth = json.load(f)
            f.close()
            
        
        sess.headers.update({
            "Authorization": f"Bearer {saved_auth['access_token']}"
        })

        response = sess.get(ACCOUNT_URL + "/get-launcher-data?arch=amd64&os=windows")
        if response.status_code == 200:
            return

    code_verifier, code_challenge = generate_pkce()
    
    port = 36445
    
    state_data = {"state": secrets.token_urlsafe(32), "port": str(port)}
    state_encoded = base64.b64encode(json.dumps(state_data).encode()).decode()
    
    authorization_url, _ = client.create_authorization_url(
        AUTH_URL,
        code_challenge=code_challenge,
        code_challenge_method='S256',
        access_type='offline',
        scope='openid offline auth:launcher',
        state=state_encoded
    )
    
    print(f"Go to: {authorization_url} to authenticate")

    server = HTTPServer(('127.0.0.1', port), CallbackHandler)
    server.handle_request()
    authorization_code = CallbackHandler.auth_code
    
    response = sess.post(
        TOKEN_URL,
        data={
            "code": authorization_code,
            "code_verifier": code_verifier,
            "grant_type": "authorization_code",
            "client_id": CLIENT_ID,
            "redirect_uri": "https://accounts.hytale.com/consent/client",
        }
    )
    
    data = response.json()
    
    token = data["access_token"]

    with open("savedauth.json", "w") as f:
        json.dump(data, f, indent=4)
        f.close()

    sess.headers.update({"Authorization": f"Bearer {token}"})
    
def select_profile():
    profiles = [{"name": x["username"],"uuid": x["uuid"],"skin": x["skin"]} for x in sess.get(ACCOUNT_URL + "/get-launcher-data?arch=amd64&os=windows").json()["profiles"]] 
    selected_profile = None

    print("Which profile do you want to use?")

    for i, profile in enumerate(profiles):
        print(f"{i + 1}. {profile['name']} ({profile['uuid']})")
    
    choice = int(input("Enter the number: ")) - 1

    selected_profile = profiles[choice]
    print(f"Selected profile: {selected_profile['name']} ({selected_profile['uuid']})")

    response = sess.post(SESSION_URL, json={
        "uuid": selected_profile["uuid"]
    }).json()
    
    identity = response["identityToken"]
    session_token = response["sessionToken"]

    sess.headers.update({
        "Authorization": f"Bearer {session_token}"
    })

    return sess, {
        "skin": json.loads(selected_profile["skin"])
    }

session_data = None

def get_data():
    global session_data
    if not session_data:
        get_token()
    
    return select_profile()