def block_areas_to_string(block_areas):
    blocks = [f'{block["lat"]},{block["lng"]},{block["radius"]}' for block in block_areas]
    return ';'.join(blocks)


def mark_waypoints(coordinates):
    return [{'lng': coords[1], 'lat': coords[0]} for coords in coordinates]
