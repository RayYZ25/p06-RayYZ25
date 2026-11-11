from io import BytesIO

from PIL import Image

from thumbor.config import Config
from thumbor.context import Context
from thumbor.engines.pil import Engine


def make_binary_alpha_palette_gif():
    # Palette GIF with index 0 as the transparent background and
    # index 1 as the blue disc. Transparency is set explicitly so the
    # source really has a transparent index.
    img = Image.new("P", (40, 40), 0)
    img.putpalette([0, 0, 0, 30, 120, 255] + [0, 0, 0] * 254)
    for x in range(10, 30):
        for y in range(10, 30):
            img.putpixel((x, y), 1)
    buf = BytesIO()
    img.save(buf, "GIF", transparency=0)
    return buf.getvalue()


def test_resized_palette_gif_keeps_transparent_index():
    config = Config(
        PILLOW_PRESERVE_INDEXED_MODE=True, ALLOW_ANIMATED_GIFS=False
    )
    engine = Engine(Context(config=config))
    engine.extension = ".gif"
    engine.image = engine.create_image(make_binary_alpha_palette_gif())
    engine.resize(20, 20)

    result = engine.read(".gif")
    out = Image.open(BytesIO(result))
    rgba = out.convert("RGBA")
    transparent = sum(1 for p in rgba.getdata() if p[3] == 0)

    assert out.info.get("transparency") is not None
    assert transparent > 0
