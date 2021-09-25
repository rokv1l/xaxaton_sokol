def colorize(route, color):
    for point in route:
        point['color'] = color
    return route
