import jinja2
from flask import Flask

app = Flask(__name__)

env = jinja2.Environment(
    loader=jinja2.PackageLoader('issues', 'templates'),
    autoescape=jinja2.select_autoescape(['html', 'xml'])
)

template = env.get_template('index.html')

@app.route("/board")
def display_board():
    return template.render()
                      
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8070)
    #app.run(host='pi2.int.franklinscott.com', port=8070)