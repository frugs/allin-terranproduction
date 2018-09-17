import io
import json
import flask
import terranproduction

try:
    from google.cloud import datastore
    FIREBASE_CONFIG = json.loads(datastore.Client().get(
        datastore.key.Key("Config", "firebaseConfig"))["value"])
except Exception:
    with open("firebaseConfig.json") as local_config:
        FIREBASE_CONFIG = json.load(local_config)

app = flask.Flask(__name__)


@app.route("/")
def index():
    return flask.render_template("index.html.j2")


@app.route("/upload", methods=["POST"])
def upload():
    if flask.request.files:
        file = next(flask.request.files.values(), None)
        replay_name = file.filename
        replay_data_stream = file.stream
    elif flask.request.data:
        replay_name = ""
        replay_data_stream = io.BytesIO(flask.request.data)
    else:
        return flask.abort(400)

    temp_file = terranproduction.util.write_to_temporary_file(replay_data_stream)
    analysis_data = terranproduction.replay.analyse_replay_file(replay_name, temp_file)
    temp_file.close()

    terranproduction.database.post_analysis(FIREBASE_CONFIG, analysis_data)

    return flask.redirect(
        flask.url_for(show_analysis.__name__, replay_id=analysis_data["replay_id"]))


@app.route("/<replay_id>")
def show_analysis(replay_id: str):
    analysis_data = terranproduction.database.get_analysis(FIREBASE_CONFIG, replay_id)
    return flask.render_template("analysis.html.j2", analysis_data=analysis_data)
