Just a little program I made out of boredom that uses the LastFM api to get the song that you're currently listening to on spotify and set that as your Instagram bio and profile picture

The program will create a server at [this](127.0.0.1:8888) address that you can manually control it with

# Installation
Before installing you first need:
1. An Instagram account
2. A LastFM account linked to your spotify
3. A LastFM API account ([click here](https://www.last.fm/api/account/create))

Once you have this info you can run these commands in the Windows command prompt
```
git clone https://github.com/suphuss/spotify-as-instagram-bio.git
cd spotify-as-instagram-bio
setup.bat
```

In the `setup.bat` file you will need to input:
1. Instagram username and password (self explanatory)
2. LastFM API key (you can find this after creating an api account)
3. LastFM username (the username attached to your LastFM account)
4. Default profile picture (the path to the picture you want to use as your profile picture when not listening to anything)
