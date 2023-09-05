import pytest
from fixture import (
    Fixture,
    FixtureSpec,
    MasterDimmer,
    NoFunction,
    StrobeSpeed,
    OverlappingValues,
)


def test_fixture_spec_shows_0_channels_if_does_not_implement_any_function():
    spec = FixtureSpec("test", "test", [])
    assert spec.channels() == 0


def test_fixture_spec_shows_unique_channels():
    spec = FixtureSpec(
        "test",
        "test",
        [
            NoFunction(6, 0, 9),
            StrobeSpeed(6, 10, 255, (1, 22)),
            NoFunction(7, 0, 50),
        ],
    )
    assert spec.channels() == 2


def test_fixtire_spec_channel_values_are_overlapping_raises_exception():
    with pytest.raises(OverlappingValues):
        FixtureSpec(
            "test",
            "test",
            [
                NoFunction(6, 0, 10),
                StrobeSpeed(6, 10, 255, (1, 22)),
            ],
        )


def test_fixtire_spec_channel_values_are_non_overlapping():
    spec = FixtureSpec(
        "test",
        "test",
        [
            NoFunction(6, 0, 9),
            StrobeSpeed(6, 10, 255, (1, 22)),
        ],
    )
    assert spec.channel_values_are_non_overlapping()


def test_fixture_channels_in_use_returns_expected_channels():
    spec = FixtureSpec(
        "test",
        "test",
        [
            NoFunction(6, 0, 9),
            StrobeSpeed(6, 10, 255, (1, 22)),
            NoFunction(7, 0, 50),
        ],
    )
    fixture = Fixture(10, spec)

    # 10 + 6; 10 + 7
    assert fixture.channels_in_use() == [16, 17]


def test_fixture_channels_in_use_returns_sorted_channels():
    spec = FixtureSpec(
        "test",
        "test",
        [
            NoFunction(7, 0, 50),
            NoFunction(6, 0, 9),
            NoFunction(7, 51, 100),
            StrobeSpeed(6, 10, 255, (1, 22)),
        ],
    )
    fixture = Fixture(100, spec)

    # 100 + 6; 100 + 7
    assert fixture.channels_in_use() == [106, 107]


def test_fixture_dimmer_returns_master_dimmer_when_supported():
    spec = FixtureSpec(
        "test",
        "test",
        [
            NoFunction(6, 0, 9),
            MasterDimmer(7, 0, 50),
            NoFunction(7, 51, 100),
        ],
    )
    fixture = Fixture(100, spec)
    dimmer = fixture.dimmer()
    assert isinstance(dimmer, MasterDimmer)
    assert dimmer.channel == 7
    assert dimmer.start_value == 0
    assert dimmer.end_value == 50
