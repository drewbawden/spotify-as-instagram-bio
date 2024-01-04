@echo off

python -m pip install -r requirements.txt

echo:
echo:

set /P IG_USERNAME=Enter Instagram username: 
set /P IG_PASSWORD=Enter Instagram password: 
set /P LASTFM_API=Enter LastFM api: 
set /P LASTFM_USERNAME=Enter LastFM username: 
set /P PFP=Enter default profile picture path: 
set /P SONG_PFP=Enter path for album profile pictures: 

echo IG_USERNAME="%IG_USERNAME%" > .env
echo IG_PASSWORD="%IG_PASSWORD%" >> .env
echo LASTFM_API="%LASTFM_API%" >> .env
echo LASTFM_USERNAME="%LASTFM_USERNAME%" >> .env
echo PFP="%PFP%" >> .env
echo SONG_PFP="%SONG_PFP%" >> .env

echo python server.py > run.bat