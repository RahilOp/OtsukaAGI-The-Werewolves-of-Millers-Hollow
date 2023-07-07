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

@app.route('/index_japanese')
def index0():
    return render_template('index_japanese.html', text='')

@app.route('/takashi')
def index1():
    return render_template('takashi.html', text='')

@app.route('/yumi')
def index2():
    return render_template('yumi.html', text='')

@app.route('/satoshi')
def index3():
    return render_template('satoshi.html', text='')

@app.route('/ayumi')
def index4():
    return render_template('ayumi.html', text='')

@app.route('/yusuke')
def index5():
    return render_template('yusuke.html', text='')

@app.route('/kazuki')
def index6():
    return render_template('kazuki.html', text='')

@app.route('/simulation')
def index7():
    return render_template('simulation_logs.html', text='')

@app.route('/well')
def index8():
    return render_template('well.html', text='')

@app.route('/haya1')
def index9():
    return render_template('haya1.html', text='')

@app.route('/haya2')
def index10():
    return render_template('haya2.html', text='')

@app.route('/haya3')
def index11():
    return render_template('haya3.html', text='')

@app.route('/haya4')
def index12():
    return render_template('haya4.html', text='')

@app.route('/college')
def index13():
    return render_template('college.html', text='')

@app.route('/shrine')
def index14():
    return render_template('shrine.html', text='')

@app.route('/yamamoto_residence')
def index15():
    return render_template('yamamoto_residence.html', text='')

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
    file_path.append("well.html")
    file_path.append("haya1.html")
    file_path.append("haya2.html")
    file_path.append("haya3.html")
    file_path.append("haya4.html")
    file_path.append("college.html")
    file_path.append("shrine.html")
    file_path.append("yamamoto_residence.html")

    
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
