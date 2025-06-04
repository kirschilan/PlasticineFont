'''from plasticinefont.renderer import generate_text_image
from io import BytesIO

def handler(request, response):
    text = request.args.get("text", "WAY TO GO")
    spacing = int(request.args.get("spacing", 10))

    output = BytesIO()
    generate_text_image(
        text=text,
        output_stream=output,
        spacing=spacing
    )

    output.seek(0)
    response.status_code = 200
    response.headers["Content-Type"] = "image/png"
    response.body = output.read()
    return response
'''
def handler(request, response):
    response.status_code = 200
    response.body = "pong"
    return response
