def colorize(route, color):
    for point in route['waypoints']:
        point['color'] = color
    return route
