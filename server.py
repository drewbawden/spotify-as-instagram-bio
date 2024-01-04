from flask import Flask, request, render_template
from multiprocessing import Process
from dotenv import load_dotenv
from instagrapi import Client
from art import tprint
import requests
import schedule
import signal
import time
import os

load_dotenv()

app = Flask(__name__)

cl = Client()
cl.login(os.getenv("IG_USERNAME"), os.getenv("IG_PASSWORD"))


############### SCHEDULER FUNCIONS ###############
def update_loop():
    print("UPDATING")
    update_info()


schedule.every(90).seconds.do(update_loop)


def run_scheduler():
    while 1:
        schedule.run_pending()
        time.sleep(1)


############### LASTFM FUNCTIONS ###############
def get_current_track():
    FM_API_KEY = os.getenv("LASTFM_API")
    FM_USERNAME = os.getenv("LASTFM_USERNAME")
    url = f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={FM_USERNAME}&api_key={FM_API_KEY}&format=json&limit=1"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        recent_tracks = data["recenttracks"]["track"]

        if recent_tracks:
            current_track = recent_tracks[0]
            try:
                current_track["@attr"]["nowplaying"]
            except:
                reset_bot()
            else:
                name = current_track["name"]
                artist = current_track["artist"]["#text"]
                image = current_track["image"][3]["#text"]
                return (name, artist, image)
        else:
            print("No recent tracks found.")
    else:
        print(f"Error: {response.status_code}, {response.text}")


############### INSTAGRAM FUNCTIONS ###############
def change_bio(bio_text):
    cl.account_edit(biography=bio_text)
    print(f"Updated bio: \n{bio_text}")


def change_pfp(image_path):
    try:
        if "http" in image_path:
            img_response = requests.get(image_path)
            if img_response.status_code == 200:
                with open("album_artwork.png", "wb") as f:
                    f.write(img_response.content)
                image_path = "album_artwork.png"
            else:
                return
    except TypeError:
        print("Not playing any muisc")

    cl.account_change_picture(image_path)


############### FLASK FUNCTIONS ###############
def update_info():
    name, artist, image = get_current_track()

    # I don't know how newlines and tabs work on instagram bios
    # I just know that this does what I need and thats good enough
    bio_text = f"""
    Listening to:
    Song: {name}
    Artist: {artist}
    """
    if len(bio_text) <= 120:
        bio_text += "\nJust cause I can"

    change_bio(bio_text)
    change_pfp(image)


def bio_input(text_input):
    print(f"Bio button clicked with input: {text_input}")
    change_bio(text_input)


def reset_bot():
    change_pfp(os.getenv("PFP"))
    change_bio("")
    tprint("RESET")


def stop_bot():
    # I don't actually know if this works, it probably does
    scheduler_process.terminate()
    scheduler_process.join()

    reset_bot()
    tprint("STOPPING")

    # forefully self die because its easier than exiting flask
    os.kill(os.getpid(), signal.SIGTERM)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/button_click", methods=["POST"])
def button_click():
    button_clicked = request.form["button"]
    if button_clicked == "update":
        update_info()
    elif button_clicked == "bio":
        text_input = request.form["text_input"]
        bio_input(text_input)
    elif button_clicked == "reset":
        reset_bot()
    elif button_clicked == "stop":
        stop_bot()

    return render_template("index.html")


if __name__ == "__main__":
    scheduler_process = Process(target=run_scheduler)
    scheduler_process.start()

    app.run(port=8888)
