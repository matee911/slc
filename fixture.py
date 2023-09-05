from dataclasses import dataclass
from itertools import groupby


class OverlappingValues(ValueError):
    pass


class FunctionNotSupported(RuntimeError):
    pass


@dataclass
class Function:
    channel: int
    start_value: int
    end_value: int
    span: None | tuple[int, int] = None

    def channel_addr(self, fixture_addr: int) -> int:
        return fixture_addr + self.channel


@dataclass
class MasterDimmer(Function):
    pass


@dataclass
class RedLight(Function):
    pass


@dataclass
class GreenLight(Function):
    pass


@dataclass
class BlueLight(Function):
    pass


@dataclass
class WhiteLight(Function):
    pass


@dataclass
class NoFunction(Function):
    pass


@dataclass
class StrobeSpeed(Function):
    pass


@dataclass
class StaticColorSelection(Function):
    pass


@dataclass
class ColorJumping(Function):
    pass


@dataclass
class ColorGradualChange(Function):
    pass


@dataclass
class ColorPulseChange(Function):
    pass


@dataclass
class SoundActiveMode(Function):
    pass


@dataclass
class FixtureSpec:
    brand: str
    model: str
    functions: list[Function]

    def __post_init__(self):
        self.channel_values_are_non_overlapping()

    def channel_values_are_non_overlapping(self) -> bool:
        # Do we have non overlapping values on each channel?
        sorted_channels = sorted(self.functions, key=lambda f: f.channel)
        for ch, group in groupby(sorted_channels, lambda f: f.channel):
            ch_values = []
            for func in group:
                ch_values.extend(range(func.start_value, func.end_value + 1))
            if len(ch_values) != len(set(ch_values)):
                raise OverlappingValues(
                    f"[{self.brand} - {self.model}] Channel {ch} has functionalities with overlapping values"
                )
        return True

    def channels(self) -> int:
        return len({func.channel for func in self.functions})


@dataclass
class Fixture:
    address: int
    spec: FixtureSpec

    def channels_in_use(self) -> list[int]:
        """
        Sorted, in ascending order, list of the channels used by the fixture with assigned address.
        """
        channels = []
        for fun in self.spec.functions:
            channels.append(fun.channel_addr(self.address))
        # We are removing dupplicated channels, because we can have multiple
        # functions on one channel, which are controlled by values
        return list(sorted(set(channels)))

    def dimmer(self) -> MasterDimmer:
        for fun in self.spec.functions:
            if isinstance(fun, MasterDimmer):
                return fun
        raise FunctionNotSupported("MasterDimmer not supported")


FIXTURE_SPECS = {
    "BBP93": FixtureSpec(
        "BeamZ",
        "BBP93",
        [
            MasterDimmer(1, 0, 255),
            RedLight(2, 0, 255),
            GreenLight(3, 0, 255),
            BlueLight(4, 0, 255),
            WhiteLight(5, 0, 255),
            NoFunction(6, 0, 9),
            StrobeSpeed(6, 10, 255, (1, 22)),
            NoFunction(7, 0, 50),
            StaticColorSelection(7, 51, 100),
            ColorJumping(7, 101, 150),
            ColorGradualChange(7, 151, 200),
            ColorPulseChange(7, 201, 250),
            SoundActiveMode(7, 251, 255),
        ],
    ),
}
