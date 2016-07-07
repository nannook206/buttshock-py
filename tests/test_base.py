import pytest
from buttshock.errors import ButtshockIOError
import buttshock.et312

# TODO create box-only test for disconnecting and resyncing in the middle of a
# message

# TODO create box-only test decorator

# TODO create emulator-only test decorator

# TODO create both test decorator

# TODO create box-only test for peeking before key exchange

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

