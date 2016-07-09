import pytest
from buttshock.errors import ButtshockIOError
import buttshock.et312
import os


no_setup = False
et312 = None


def run_box_test(func):
    global et312
    if et312 is not None:
        pytest.fail("Global connection object not cleared before new test run!")
    with buttshock.et312.ET312SerialSync(os.environ["BUTTSHOCK_SERIAL_PORT"]) as et:
        et312 = et
        func()
    et312 = None


def run_emulator_test(func):
    global et312
    with buttshock.et312.ET312EmulatorSync() as et:
        et312 = et
        func()
    et312 = None


def no_setup(func):
    def func_wrapper():
        global no_setup
        no_setup = True
        func()
        no_setup = False
    return func_wrapper


def box_only(func):
    def func_wrapper():
        global no_setup, et312
        if "BUTTSHOCK_SERIAL_PORT" not in os.environ.keys():
            pytest.skip("Box only test, skipping.")
        if not no_setup:
            run_box_test(func)
        else:
            func()
    return func_wrapper


def emulator_only(func):
    def func_wrapper():
        global no_setup, et312
        if "BUTTSHOCK_SERIAL_PORT" in os.environ.keys():
            pytest.skip("Emulator only test, skipping.")
        if not no_setup:
            run_emulator_test(func)
        else:
            func()
    return func_wrapper


def box_or_emulator(func):
    def func_wrapper():
        global no_setup, et312
        if not no_setup:
            if "BUTTSHOCK_SERIAL_PORT" in os.environ.keys():
                run_box_test(func)
            else:
                run_emulator_test(func)
    return func_wrapper

# TODO create box-only test for disconnecting and resyncing in the middle of a
# message

# TODO create box-only test for peeking before key exchange


@emulator_only
def test_emulator():
    assert et312.key == (et312.port.emu.box_key ^ 0x55)


@no_setup
@box_or_emulator
def test_missing_serial():
    import serial
    with pytest.raises(serial.serialutil.SerialException):
        buttshock.et312.ET312SerialSync("not-a-port")


@no_setup
@box_or_emulator
def test_wrong_serial():
    with pytest.raises(ButtshockIOError):
        buttshock.et312.ET312SerialSync(1)


@no_setup
@box_only
def test_box_reconnect():
    with buttshock.et312.ET312SerialSync(os.environ["BUTTSHOCK_SERIAL_PORT"]) as et:
        assert(et.get_current_mode() == 0)
    with buttshock.et312.ET312SerialSync(os.environ["BUTTSHOCK_SERIAL_PORT"]) as et:
        assert(et.get_current_mode() == 0)
