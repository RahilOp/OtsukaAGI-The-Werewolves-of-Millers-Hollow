from flask import Flask, render_template, Markup, Response
import time

# app = Flask(__name__)


# @app.route('/')
# def display_text():
#     # Read the text from the file
#     with open('text.txt', 'r') as file:
#         text = file.read()

#     text = text.replace('\n', '<br>')
#     # Apply color to the text
#     colored_content = '<span style = "color: red ">{}</span>'.format(text)

#     safe_html_content = Markup(colored_content)
#     # Render the text within an HTML template
#     return render_template('index.html', text=safe_html_content)



# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', text='')

@app.route('/get-text')
def get_text():
    # Replace this logic with your own code to fetch and return the updated text
    # Read the text from the file
    file_path = []

    file_path.append("text1.html")
    file_path.append("text2.html")
    file_path.append("text3.html")
    file_path.append("text4.html")
    file_path.append("text5.html")
    file_path.append("text6.html")
    file_path.append("simulation.html")
    
    texts = []

    for i in range(0,len(file_path)):
        with open(file_path[i], 'r') as file:
            texts.append(file.read())
    
    safe_html_contents = []
    for i in range(0,len(texts)):
        texts[i] = texts[i].replace('\n', '<br>')
        # Apply color to the text
        safe_html_contents.append(Markup(texts[i]))

    return safe_html_contents

@app.route('/updates')
def updates():
    def generate_updates():
        # Replace this logic with your own code to generate and yield the updated logs
        yield 'Updated Logs 1\n'
        yield 'Updated Logs 2\n'
        yield 'Updated Logs 3\n'

    return Response(generate_updates(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)
