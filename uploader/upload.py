import base64
import gzip
import json
import tempfile
from typing import Callable

import sc2reader
import techlabreactor
from aiohttp.web_exceptions import HTTPFound
from aiohttp.web_request import Request
from aiohttp.web_response import Response

from uploader.serialiser import serialise_chart_data

CHUNK_SIZE = 1024


def _compress_and_encode(data: str) -> str:
    compressed = gzip.compress(data.encode())
    return base64.b64encode(compressed).decode()


class ReplayUploader:

    def __init__(self, redirect_supplier: Callable[[str], str]):
        self.redirect_supplier = redirect_supplier

    async def upload_replay(self, request: Request) -> Response:

        if request.content_type.startswith("multipart/"):
            reader = await request.multipart()
            replay_data = await reader.next()
            replay_name = replay_data.filename
        else:
            replay_name = ""
            replay_data = request.content

        if replay_data is None:
            return Response(body="Invalid Replay", status=402)

        with tempfile.TemporaryFile() as replay_file:
            while True:
                chunk = await request.content.read(CHUNK_SIZE)
                if not chunk:
                    break

                replay_file.write(chunk)

            replay_file.seek(0)

            try:
                replay = sc2reader.load_replay(replay_file)

                data = {
                    "players": [],
                    "replayName": replay_name
                }
                for player in replay.players:
                    production_capacity = techlabreactor.production_capacity_till_time_for_player(
                        600, player, replay)
                    production_usage = techlabreactor.production_used_till_time_for_player(
                        600, player, replay)
                    supply_blocks = techlabreactor.get_supply_blocks_till_time_for_player(
                        600, player, replay)

                    if production_capacity and production_usage:
                        data["players"].append({
                            "name": player.name,
                            "structureTypes": list(production_capacity.keys()),
                            "chartData": serialise_chart_data(production_capacity, production_usage, supply_blocks),
                        })

            except Exception as e:
                return Response(body="Invalid Replay\n" + str(e), status=402)

        param = _compress_and_encode(json.dumps(data))
        return HTTPFound(self.redirect_supplier(param))
