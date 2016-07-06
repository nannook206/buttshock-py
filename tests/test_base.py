import pytest
from buttshock.errors import ButtshockIOError
import buttshock.et312


def test_emulator():
    with buttshock.et312.ET312EmulatorSync() as et312:
        assert et312.key == (et312.port.emu.box_key ^ 0x55)


def test_missing_serial():
    import serial
    with pytest.raises(serial.serialutil.SerialException):
        buttshock.et312.ET312SerialSync("not-a-port")


def test_wrong_serial():
    with pytest.raises(ButtshockIOError):
        buttshock.et312.ET312SerialSync(1)
