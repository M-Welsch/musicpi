import os
import sys
from time import sleep

import pytest


from musicpi.hardware import RotaryEncoder


@pytest.mark.onraspi
def test_encoder_readout():
    encoder = RotaryEncoder()
    try:
        while True:
            print(encoder.read())
            sleep(0.5)
    except KeyboardInterrupt:
        pass
