from flask import Flask

app = Flask(__name__)  # Creates a Flask web app

@app.route("/")
def version():
    version = "V0.0.1"
    return f"The Current Version Of The App Is: {version}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
