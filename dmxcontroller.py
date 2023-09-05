import struct
import numpy as np

import serial
import serial.rs485

from fixture import Fixture

DMXPacket = struct.Struct("512B")


def dmx_pack(data):
    return DMXPacket.pack(*data).ljust(512, b"\x00")


class Universe:
    def __init__(self, dmx: str, fixtures: list[Fixture] | None = None):
        """

        :param port: USB device address; see python -m serial.tools.list_ports
        """
        self._blocking_mode = False
        self._commands = []
        self.channels = 512
        self.fixtures = fixtures or []

    def __enter__(self):
        self._blocking_mode = True

    def __exit__(self, exc_type, exc_value, traceback):
        self._blocking_mode = False
        self._commands = []

    def normalize_value(self, value: int) -> int:
        return max(min(value, 255), 0)

    def set_channel(self, channel: int, value: int):
        value = self.normalize_value(value)
        self._commands.append(channel, value)
        if not self._blocking_mode:
            self.flush()

    def flush(self):
        for cmd in self._commands:
            ser.write()


def client(port: str | None = None) -> serial.Serial:
    ser = serial.Serial(...)
    ser.rs485_mode = serial.rs485.RS485Settings(...)
    return ser


def mysine(t, amp, freq, phi, shift) -> np.ndarray:
    """
    Solves the sine wave equation;

    f(t; ) = sin*2*np*freq*t + phi), where

    amp is the wave amplitude,
    freq is the wave frequency,
    phi is the phase shift,

    and t (time) the independent variable

    Credits:
    https://notebook.community/JoseGuzman/myIPythonNotebooks/SignalProcessing/Sine%20waves%20and%20complex%20waves
    https://www.dummies.com/article/academics-the-arts/math/trigonometry/shift-a-sine-function-in-a-graph-187133/
    """
    return (amp * np.sin(2 * np.pi * freq * t + phi)) + shift


def demo_lights_functions(channels: int = 3) -> list[np.ndarray]:
    """

    :param channels: Depending on the type of fixture we are talking about RGB/RGBW/RGBWA/RGBWA-UV. Default 3 as bare minimum.
    :return:

    >>> t, arrays = demo_lights_functions(6)
    >>> for a in arrays:
    ...     plt.plot(t, a)

    """
    freq = 1 / 44  # Max RS485 frequency
    t = np.arange(0, 255, freq)
    amp = 256 / 2
    shift = amp
    _channels = []
    for i in range(channels):
        phi = i * 2
        # Starts from i=0 so 1/3; i=1 -> 1/4
        freq_coef = 1 / (i + 3)
        _channels.append(
            mysine(t, amp=amp, freq=freq * freq_coef, phi=phi, shift=shift)
        )
    return t, _channels


def demo_lights_values_generator(channels: int = 3):
    t, arrays = demo_lights_functions(channels)
    for values in zip(*arrays):
        yield tuple(round(v) for v in values)
