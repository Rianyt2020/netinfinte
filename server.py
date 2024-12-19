import os
import base64
import eyed3
from flask import Flask, jsonify, render_template, send_from_directory, request
import datetime

# Initialize Flask app
app = Flask(__name__)

# Paths to Song Folders and Static Files
SONG_FOLDER = '/data/data/com.termux/files/home/storage/shared/1NetInfinte/static/songs'
PREMIUM_SONG_FOLDER = '/data/data/com.termux/files/home/storage/shared/1NetInfinte/static/permusic'
STATIC_FOLDER = '/data/data/com.termux/files/home/storage/shared/1NetInfinte/static'

# Variable to store the like count
like_count = 0

# Log user visits to the app
@app.before_request
def log_visit():
    user_ip = request.remote_addr  # Get user's IP address
    visit_time = datetime.datetime.now()  # Get the current time
    log_message = f"New visit: IP = {user_ip}, Time = {visit_time}\n"

    # Write the log message to a text file
    with open("visit_log.txt", "a") as log_file:
        log_file.write(log_message)

# General Routes for Songs
@app.route('/')
def home_page():
    return render_template('songs.html')

@app.route('/api/songs')
def get_songs():
    return get_song_list(SONG_FOLDER)

@app.route('/static/songs/<filename>')
def serve_song(filename):
    return serve_file(SONG_FOLDER, filename)

# Premium Song Routes
@app.route('/premium')
def premium_page():
    return render_template('premium.html')

@app.route('/api/premium_songs')
def get_premium_songs():
    return get_song_list(PREMIUM_SONG_FOLDER)

@app.route('/static/permusic/<filename>')
def serve_premium_song(filename):
    return serve_file(PREMIUM_SONG_FOLDER, filename)

# About Us Page
@app.route('/about')
def about_page():
    return render_template('about.html')

# Contact Page
@app.route('/contact')
def contact_page():
    return render_template('contact.html')

# Help Page
@app.route('/help')
def help_page():
    return render_template('help.html')

# Privacy Policy Page
@app.route('/privacy-policy')
def privacy_policy_page():
    return render_template('privacy-policy.html')

# Services Page
@app.route('/services')
def services_page():
    return render_template('services.html')

# Videos Page
@app.route('/videos')
def videos_page():
    return render_template('videos.html')

# Latest Page
@app.route('/latest')
def latest_page():
    return render_template('latest.html')

# Rate Page
@app.route('/rate')
def rate_page():
    return render_template('rate.html')

# Route to get the like count
@app.route('/get_likes', methods=['GET'])
def get_likes():
    return jsonify({'likes': like_count})

# Route to like the website
@app.route('/like', methods=['POST'])
def like():
    global like_count
    like_count += 1
    return jsonify({'likes': like_count})

# Helper to Get Song List with Metadata
def get_song_list(folder):
    try:
        songs = []
        for f in os.listdir(folder):
            if f.endswith(".mp3"):
                song_info = {'name': f}
                audio_file = eyed3.load(os.path.join(folder, f))
                if audio_file and audio_file.tag:
                    song_info['artist'] = audio_file.tag.artist or 'Unknown Artist'
                    song_info['title'] = audio_file.tag.title or 'Unknown Title'
                    if audio_file.tag.images:
                        image = audio_file.tag.images[0].image_data
                        song_info['image'] = f"data:image/jpeg;base64,{base64.b64encode(image).decode('utf-8')}"
                    else:
                        song_info['image'] = "/static/images/L2.jpg"
                else:
                    song_info.update({'artist': 'Unknown Artist', 'title': 'Unknown Title', 'image': "/static/images/L2.jpg"})
                songs.append(song_info)
        return jsonify(songs)
    except Exception as e:
        return jsonify({"error": str(e)})

# Helper to Serve Files
def serve_file(folder, filename):
    try:
        return send_from_directory(folder, filename)
    except Exception as e:
        return str(e)

# Run Flask App
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)