from plasticinefont.renderer import generate_text_image
from io import BytesIO
import base64

def handler(request):
    text = request.args.get("text", "WAY TO GO")
    spacing = int(request.args.get("spacing", 10))

    output = BytesIO()
    generate_text_image(
        text=text,
        output_stream=output,
        spacing=spacing
    )

    output.seek(0)
    image_bytes = output.read()

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "image/png"
        },
        "body": base64.b64encode(image_bytes).decode("utf-8"),
        "isBase64Encoded": True
    }
