from thumbor.ext.filters import _round_corner

WIDTH = 40
HEIGHT = 40
RADIUS = 10


def test_transparent_round_corner_edge_is_not_dark():
    source = bytes([255, 255, 255, 255]) * (WIDTH * HEIGHT)
    out = _round_corner.apply(
        1, "RGBA", RADIUS, RADIUS, 0, 0, 0, WIDTH, HEIGHT, source, 1
    )
    pixels = [out[i : i + 4] for i in range(0, len(out), 4)]
    visible = [p for p in pixels if p[3] > 0]
    dark = [p for p in visible if p[0] != 255 or p[1] != 255 or p[2] != 255]
    partial = [p for p in visible if p[3] < 255]
    assert dark == []
    assert partial
