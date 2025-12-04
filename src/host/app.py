from flask import Flask, send_from_directory
from alarm import AlarmHost

app = Flask(__name__)
host = AlarmHost()

@app.route("/")
def home():
    return "Test"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)