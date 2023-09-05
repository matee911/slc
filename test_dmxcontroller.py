from dmxcontroller import Universe


def test_normalized_value_if_no_lower_than_0():
    universe = Universe("x")
    assert dmx.normalize_value(-1) == 0
    assert dmx.normalize_value(0) == 0


def test_normalized_value_if_no_higher_than_255():
    universe = Universe("x")
    assert dmx.normalize_value(256) == 255
    assert dmx.normalize_value(255) == 255
