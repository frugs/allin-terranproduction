import asyncio
import json

import pyrebase


def open_db_connection(db_config: dict) -> pyrebase.pyrebase.Database:
    return pyrebase.initialize_app(db_config).database()


async def post_analysis(db_config: dict, analysis_data: dict) -> str:
    replay_id = analysis_data["replay_id"]

    def post_analysis_inner():
        db = open_db_connection(db_config)
        db.child("terran_production_analyses").child(replay_id).set(json.dumps(analysis_data))
    await asyncio.get_event_loop().run_in_executor(None, post_analysis_inner)

    return replay_id


async def get_analysis(db_config: dict, replay_id: str) -> str:
    def get_analysis_inner():
        db = open_db_connection(db_config)
        analysis_data = db.child("terran_production_analyses").child(replay_id).get().val()
        return analysis_data if analysis_data else {}

    return await asyncio.get_event_loop().run_in_executor(None, get_analysis_inner)
