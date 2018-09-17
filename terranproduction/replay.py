from typing import Dict, IO, List, Tuple

import sc2reader
import techlabreactor


def serialise_chart_data(production_capacity: Dict[str, List[Tuple[float, int]]],
                         production_usage: Dict[str, List[Tuple[float, int]]],
                         supply_blocks: List[Tuple[float, bool]]) -> list:

    chart_data = []
    offset = 0
    for structure_type in production_capacity.keys():

        capacity_data = []
        for second, capacity in production_capacity[structure_type]:
            capacity_data.append([int(second * 1000), capacity + offset])

        usage_base_line = [capacity_data[0]]
        for second, usage in production_usage.get(structure_type, []):
            usage_base_line.append([int(second * 1000), offset])

        usage_data = [capacity_data[0]]
        for second, usage in production_usage.get(structure_type, []):
            usage_data.append([int(second * 1000), usage + offset])

        chart_data.append(usage_base_line)
        chart_data.append(usage_data)
        chart_data.append(capacity_data)

        offset += 2 + max(map(lambda x: x[1], production_capacity[structure_type]))

    supply_block_data = []
    was_blocked = False
    for second, blocked in supply_blocks:
        if not was_blocked and blocked:
            supply_block_data.append([int(second * 1000), 0])

        if was_blocked and not blocked:
            supply_block_data.append([int(second * 1000), 0])
            supply_block_data.append([int(second * 1000), "NaN"])

        if blocked:
            supply_block_data.append([int(second * 1000), offset])

        was_blocked = blocked

    chart_data.append(supply_block_data)

    return chart_data


def analyse_replay_file(replay_name: str, replay_file: IO[bytes]) -> dict:
    replay = sc2reader.SC2Reader().load_replay(replay_file)

    data = {"replay_id": replay.filehash, "players": [], "replayName": replay_name}
    for player in replay.players:
        production_capacity = techlabreactor.production_capacity_till_time_for_player(
            600, player, replay)
        production_usage = techlabreactor.production_used_till_time_for_player(600, player, replay)
        supply_blocks = techlabreactor.get_supply_blocks_till_time_for_player(600, player, replay)

        if production_capacity and production_usage:
            data["players"].append({
                "name":
                player.name,
                "structureTypes":
                list(production_capacity.keys()),
                "chartData":
                serialise_chart_data(production_capacity, production_usage, supply_blocks),
            })
    return data
