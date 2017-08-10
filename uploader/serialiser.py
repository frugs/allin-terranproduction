from typing import Dict, List, Tuple


def serialise_chart_data(
        production_capacity: Dict[str, List[Tuple[float, int]]],
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
