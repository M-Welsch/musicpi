import os
import sys
from typing import Generator

import pytest

from musicpi.hardware.display import Display


@pytest.fixture
def display() -> Generator[Display, None, None]:
    yield Display()


@pytest.mark.onraspi
def test_display_init(display):
    display.write_teststuff_to_displays()
