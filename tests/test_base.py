import sys
import os

try:
    import buttshock
except:
    sys.path.append(os.path.join(os.path.realpath(__file__), ".."))
    import buttshock


def test_emulator():
    with buttshock.ButtshockET312EmulatorSync() as et312:
        assert et312.key == (et312.port.emu.box_key ^ 0x55)
