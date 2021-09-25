def colorize(route, color):
    _route = route
    for point in _route:
        point['color'] = color
    return _route
