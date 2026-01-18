ACCOUNT_URL = "https://account-data.hytale.com/my-account"
PROFILES_URL = "https://accounts.hytale.com/profiles"

import json
from auth import get_data
import os

sess, account_data = get_data()

skins = [{
    "name": skin[:-5],
    "path": os.path.join("skins", skin)
} for skin in os.listdir("skins") if skin.endswith(".json")]

print("Select mode: ")
print("\t1. Extract Skin")
print("\t2. Upload Skin")

mode = int(input("Enter mode number: "))

if mode == 1:
    name = input("Enter name for extracted skin: ")

    skin_data = account_data["skin"]

    with open(os.path.join("skins", f"{name}.json"), "w") as f:
        f.write(json.dumps(skin_data, indent=4))
elif mode == 2:
    print("Available skins:")
    for i, skin in enumerate(skins):
        print(f"{i + 1}: {skin['name']}")

    choice = int(input("Select a skin by number: ")) - 1
    selected_skin = skins[choice]

    with open(selected_skin["path"], "r") as f:
        skin_json = json.load(f)
        response = sess.put(ACCOUNT_URL + "/skin", json = skin_json)

        print(response.status_code, response.text)