import pytest
import pulsedive


@pytest.fixture
def pud():
    return pulsedive.Pulsedive()
