
from flask import Flask, render_template, request, redirect
import os
from datetime import datetime
import random
from PIL import Image
import colorsys
import random


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

journal_entries = []

# Fake AI caption generator
def generate_fake_caption():
    options = [
        "Lost in thought, found in pixels.",
        "Another memory, softly framed.",
        "Where silence meets the soul.",
        "Vibes too loud for words.",
        "Eyes say what hearts hide."
    ]
    return random.choice(options)
# Quote list for homepage and AI quote button
daily_quotes = [
    "You are doing better than you think.",
    "Trust the process, even when it’s quiet.",
    "Your vibe attracts your tribe.",
    "Take the picture, write the feeling.",
    "Healing isn’t linear, but it’s beautiful.",
    "Let your photos say what you can’t.",
    "You are the main character. Always."
]

# Random quote for homepage
def get_daily_quote():
    return random.choice(daily_quotes)

# Get dominant color mood
def detect_mood_color(image_path):
    img = Image.open(image_path).resize((50, 50))
    pixels = list(img.getdata())
    r, g, b = map(lambda x: sum(x) // len(pixels), zip(*pixels))
    hue = colorsys.rgb_to_hsv(r/255, g/255, b/255)[0]
    if hue < 0.1 or hue > 0.9:
        return "🔥 Passionate"
    elif hue < 0.3:
        return "💛 Warm"
    elif hue < 0.6:
        return "💚 Calm"
    else:
        return "💙 Cool"

@app.route('/', methods=['GET', 'POST'])
def index():
    quote = get_daily_quote()  # 👈 Add this line
    if request.method == 'POST':
        file = request.files['photo']
        caption = request.form['caption'] or generate_fake_caption()
        filename = datetime.now().strftime("%Y%m%d%H%M%S") + "_" + file.filename
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        mood = request.form.get("mood") or detect_mood_color(path)
        journal_entries.append({
            'photo': filename,
            'caption': caption,
            'date': datetime.now().strftime("%d %b %Y"),
            'mood': mood
        })
        return redirect('/gallery')
    return render_template('index.html', quote=quote)  # 👈 Pass the quote

@app.route('/gallery')
def gallery():
    return render_template('gallery.html', entries=journal_entries)

if __name__ == '__main__':
    app.run(debug=True)
