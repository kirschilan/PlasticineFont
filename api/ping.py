def handler(request, response):
    response.status_code = 200
    response.body = "pong"
    response.headers["Content-Type"] = "application/json"
    return response
