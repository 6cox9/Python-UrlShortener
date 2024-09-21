from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import string
import random

app = Flask(__name__)

# Function to generate a random short URL
def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(6))
    return short_url

# Route for the home page
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        original_url = request.form.get('url')

        if not original_url:
            return "Please provide a valid URL", 400

        # Generate a short URL
        short_url = generate_short_url()

        # Save original and short URL in the database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO urls (original_url, short_url) VALUES (?, ?)", (original_url, short_url))
        conn.commit()
        conn.close()

        return render_template('index.html', short_url=request.host_url + short_url)

    return render_template('index.html')

# Route to redirect the short URL to the original URL
@app.route('/<short_url>')
def redirect_url(short_url):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT original_url FROM urls WHERE short_url = ?", (short_url,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return redirect(result[0])
    else:
        return "URL not found!", 404

if __name__ == '__main__':
    app.run(debug=True)
