def handler(request, response):
    response.status_code = 200
    response.body = "pong"
    return response
