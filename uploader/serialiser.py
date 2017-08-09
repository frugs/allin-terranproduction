from typing import Dict, List, Tuple


def serialise_chart_data(
        production_capacity: Dict[str, List[Tuple[float, int]]],
        production_usage: Dict[str, List[Tuple[float, int]]]) -> list:

    chart_data = []
    offset = 0
    for structure_type in production_capacity.keys():

        usage_data = []
        for second, usage in production_usage[structure_type]:
            usage_data.append({
                "x": int(second * 1000),
                "y": usage + offset
            })

        chart_data.append(usage_data)

        capacity_data = []
        for second, capacity in production_capacity[structure_type]:
            capacity_data.append({
                "x": int(second * 1000),
                "y": capacity + offset
            })

        chart_data.append(capacity_data)

        offset += 2 + max(map(lambda x: x[1], production_capacity[structure_type]))

    return chart_data
