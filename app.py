from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    output = "Hello, World!"  # Replace with your desired Python output
    return render_template('D:\JAPAN\OTSUKA-AGI\venv\index.html', output=output)

if __name__ == '__main__':
    app.run()
