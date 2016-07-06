import buttshock.et312


def test_emulator():
    with buttshock.et312.ET312EmulatorSync() as et312:
        assert et312.key == (et312.port.emu.box_key ^ 0x55)
