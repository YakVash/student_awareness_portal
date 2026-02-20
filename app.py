from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/check', methods=['POST'])
def check():
    return "Form Submitted Successfully"

if __name__ == '__main__':
    app.run(debug=True)