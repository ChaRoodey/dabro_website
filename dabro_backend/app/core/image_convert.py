from io import BytesIO

from PIL import Image

MAX_WIDTH = 4000
MAX_HEIGHT = 4000


def convert_to_webp(file_bytes: bytes) -> bytes:
    image = Image.open(BytesIO(file_bytes))

    if image.width > MAX_WIDTH or image.height > MAX_HEIGHT:
        raise ValueError("Image resolution too large")

    image.thumbnail((400, 300))

    output = BytesIO()
    image.save(output, format='WEBP', quality=85)

    return output.getvalue()
