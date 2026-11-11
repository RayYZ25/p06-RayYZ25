from PIL import Image

from thumbor.config import Config
from thumbor.context import Context, RequestParameters
from thumbor.engines.pil import Engine
from thumbor.transformer import Transformer


def make_transformer(width, height):
    config = Config()
    context = Context(config=config)
    context.request = RequestParameters(width=width, height=height)
    context.request.engine = Engine(context)
    context.request.engine.image = Image.new("RGBA", (1, 1), (255, 0, 0, 255))
    context.request.engine.extension = ".png"
    return Transformer(context)


def test_one_pixel_source_to_wide_strip_is_not_empty():
    transformer = make_transformer(50, 25)
    transformer.context.request.engine.extension = ".png"
    transformer.img_operation_worker()

    image = transformer.engine.image
    assert image.size == (50, 25)
    pixel = image.convert("RGBA").getpixel((0, 0))
    assert pixel[3] == 255
