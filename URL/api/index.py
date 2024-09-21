from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

# Home route
@app.route("/", methods=["GET", "POST"])
def home():
    return "Hello, Vercel Flask!"

# Create an entry point for Vercel
def handler(request, context):
    return app(request.environ, start_response)
