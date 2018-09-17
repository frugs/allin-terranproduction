import json
import pyrebase


def open_db_connection(db_config: dict) -> pyrebase.pyrebase.Database:
    return pyrebase.initialize_app(db_config).database()


def post_analysis(db_config: dict, analysis_data: dict) -> str:
    replay_id = analysis_data["replay_id"]

    db = open_db_connection(db_config)
    db.child("terran_production_analyses").child(replay_id).set(json.dumps(analysis_data))

    return replay_id


def get_analysis(db_config: dict, replay_id: str) -> str:
    db = open_db_connection(db_config)
    analysis_data = db.child("terran_production_analyses").child(replay_id).get().val()
    return analysis_data if analysis_data else {}
