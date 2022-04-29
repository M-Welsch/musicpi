import os
import sys
from time import sleep

import pytest

from musicpi.hardware.pin_interface import Encoder


@pytest.mark.onraspi
def test_encoder_readout() -> None:
    encoder = Encoder()
    try:
        while True:
            print(encoder.read())
            sleep(0.5)
    except KeyboardInterrupt:
        pass
