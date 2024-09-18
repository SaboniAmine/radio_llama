from flask import Flask
import src.radio as radio
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/generate")
def generate():
    output = radio.generate_radio()
    return {
        "status": "success",
        "output": output
    }