import pytest

from np_aind_metadata import np


@pytest.mark.onprem
@pytest.mark.parametrize(
    "args",
    [
        ("NP1", ),
        ("NP2", ),
        ("NP3", ),
    ]
)
def test_init_neuropixels_rig_from_np_config(args) -> None:
    np.init_neuropixels_rig_from_np_config(*args)
