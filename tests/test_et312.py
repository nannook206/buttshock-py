import pytest
from buttshock.errors import ButtshockIOError
import buttshock.et312
import os
from functools import wraps, partial

###############################################################################
# Tests Decorators
###############################################################################

# Modeled after http://stackoverflow.com/a/10288657/4040754, these descriptors
# can take an optional kwarg that denotes whether or not an ET312 object should
# be set up before the test is run. This cleans up the testing code if we are
# running tests that expect clean connects/disconnects.


def run_test(func, no_setup):
    if no_setup:
        func()
        return
    if "BUTTSHOCK_SERIAL_PORT" in os.environ.keys():
        with buttshock.et312.ET312SerialSync(os.environ["BUTTSHOCK_SERIAL_PORT"]) as et:
            func(et312=et)
    else:
        with buttshock.et312.ET312EmulatorSync() as et:
            func(et312=et)


def box_only(func=None, no_setup=False):
    if not callable(func):
        return partial(box_only, no_setup=no_setup)

    @wraps(func)
    def wrapper(*args, **kwargs):
        if "BUTTSHOCK_SERIAL_PORT" not in os.environ.keys():
            pytest.skip("Box only test, skipping.")
        run_test(func, no_setup)
    return wrapper


def emulator_only(func=None, no_setup=False):
    if not callable(func):
        return partial(emulator_only, no_setup=no_setup)

    @wraps(func)
    def wrapper(*args, **kwargs):
        if "BUTTSHOCK_SERIAL_PORT" in os.environ.keys():
            pytest.skip("Emulator only test, skipping.")
        run_test(func, no_setup)
    return wrapper


def box_or_emulator(func=None, no_setup=False):
    if not callable(func):
        return partial(box_or_emulator, no_setup=no_setup)

    @wraps(func)
    def wrapper(*args, **kwargs):
        run_test(func, no_setup)
    return wrapper

###############################################################################
# Tests
###############################################################################

# TODO create box-only test for disconnecting and resyncing in the middle of a
# message

# TODO create box-only test for peeking before key exchange


@emulator_only
def test_emulator(et312=None):
    # TODO I'm not sure if this test is right? I think emulator key setup may
    # be wrong.
    assert et312.key == (et312.port.emu.ram[0x213])


@box_or_emulator(no_setup=True)
def test_missing_serial():
    import serial
    with pytest.raises(serial.serialutil.SerialException):
        buttshock.et312.ET312SerialSync("not-a-port")


@box_or_emulator(no_setup=True)
def test_wrong_serial():
    with pytest.raises(ButtshockIOError):
        buttshock.et312.ET312SerialSync(1)


@box_only(no_setup=True)
def test_box_reconnect():
    with buttshock.et312.ET312SerialSync(os.environ["BUTTSHOCK_SERIAL_PORT"]) as et:
        assert(et.get_current_mode() == 0)
    with buttshock.et312.ET312SerialSync(os.environ["BUTTSHOCK_SERIAL_PORT"]) as et:
        assert(et.get_current_mode() == 0)


@box_or_emulator(no_setup=True)
def test_missing_read_write():
    class MissingRW(buttshock.et312.ET312Base):
        pass
    m = MissingRW()
    with pytest.raises(RuntimeError):
        m.read(0x0)
    with pytest.raises(RuntimeError):
        m.write(0x0, [0x0])


@box_or_emulator
def test_invalid_write_type(et312=None):
    with pytest.raises(TypeError):
        et312.write(0x0, 0x0)


@box_or_emulator
def test_invalid_write_length_min(et312=None):
    with pytest.raises(ButtshockIOError):
        et312.write(0x0, [])


@box_or_emulator
def test_invalid_write_length_max(et312=None):
    with pytest.raises(ButtshockIOError):
        et312.write(0x0, [0x0] * 9)

