# Hytale-Skin-Loader
Simple python script that authenticates with Hytale's api and saves/loads saved skins

# Use

You may have to download the requirements to use this if you do not already have them
Simply install python, and run

```
pip install requests
pip install authlib 
```
OR, if you know how to open the directory in cmd/terminal/etc:
```
pip install -r requirements.txt
```


Run skin-editor.py, not auth.py. It will give you a link to open and will automatically log you in. 
If you are currently ingame, it may log you out as it has to log into the game to actually change your skin.

# Forking
If you want to make some other hytale script that requires the auth token, just rip auth.py out of this and use it for your own project. Follow GPL 3.0 (license any forks it under GPL3, keep it open-source)

This contains code to authenticate a hytale account and create session tokens without hytale's oauth limitations. This does not read or decrypt account.dat, which would be a direct violation of the ToS. This requires a browser window to be opened to authenticate, and does not abuse any APIs. 

While you're free to take auth.py and use it in your own projects, if you use it to steal accounts, run bots (i.e. mineflayer) or violate ToS in some other way, you're a dickhead.
Note auth.py uses an entirely different client id. Hytale-Server has limitations and using scope auth:server prevents you from creating a game session.

# Credits

[HTTP Toolkit](https://httptoolkit.com/)

[authlib](https://github.com/authlib/authlib) (trying to authenticate any other way is suffering nobody should endure)
