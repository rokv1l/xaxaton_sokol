def block_areas_to_string(block_areas):
    blocks = [f'{block["lat"]},{block["lng"]},{block["radius"]}' for block in block_areas]
    return ';'.join(blocks)


def mark_waypoints(coordinates):
    return [{'lng': coords[0], 'lat': coords[1]} for coords in coordinates]
