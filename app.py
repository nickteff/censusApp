import flask

app = flask.Flask(__name__)


def stream_template(template_name, **context):
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.enable_buffering(5)
    return rv


@app.route('/')
def hello_world():
    return flask.render_template("index.html", profiles=range(2000))

@app.route('/interaction', methods=['POST'])
def post_interaction():
    return flask.render_template('interaction.html')

@app.route('/interaction', methods=["GET"])
def get_interaction():
    return flask.render_template('interaction.html')

if __name__ == '__main__':
    app.run(port=5001)
