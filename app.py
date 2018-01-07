import base64
import gzip
import os
import pickle

import aiohttp.web
import aiohttp_jinja2
import jinja2
import pkg_resources

import terranproduction

FIREBASE_CONFIG = pickle.loads(gzip.decompress(base64.b64decode(os.getenv("FIREBASE_CONFIG"))))


@aiohttp_jinja2.template('index.html.j2')
async def index(_: aiohttp.web.Request) -> dict:
    return {}


@aiohttp_jinja2.template('analysis.html.j2')
async def show_analysis(request: aiohttp.web.Request) -> dict:
    replay_id = request.match_info['replay_id']
    analysis_data = await terranproduction.database.get_analysis(FIREBASE_CONFIG, replay_id)
    return {
        "analysis_data": analysis_data
    }


async def upload_analysis(request: aiohttp.web.Request) -> aiohttp.web.Response:
    if request.content_type.startswith("multipart/"):
        reader = await request.multipart()
        replay_data_stream = await reader.next()
        replay_name = replay_data_stream.filename
    else:
        replay_name = ""
        replay_data_stream = request.content

    if replay_data_stream is None:
        return aiohttp.web.HTTPClientError(body="Invalid Replay")

    temp_file = await terranproduction.util.write_to_temporary_file(replay_data_stream)
    analysis_data = await terranproduction.replay.analyse_replay_file(replay_name, temp_file)
    temp_file.close()

    await terranproduction.database.post_analysis(FIREBASE_CONFIG, analysis_data)

    return aiohttp.web.HTTPFound(analysis_data["replay_id"])


class App(aiohttp.web.Application):

    def __init__(self):
        super().__init__()

        aiohttp_jinja2.setup(self, loader=jinja2.FileSystemLoader('templates/'))

        self.router.add_get("/", index)
        self.router.add_get("/{replay_id}", show_analysis)
        self.router.add_post("/upload", upload_analysis)
        self.router.add_static('/static', pkg_resources.resource_filename(__name__, "static"))


def main():
    aiohttp.web.run_app(App(), port=32432)
    pass


if __name__ == "__main__":
    main()
