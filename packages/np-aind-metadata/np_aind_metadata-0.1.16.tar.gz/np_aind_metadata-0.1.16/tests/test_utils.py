# import pytest

# from pathlib import Path

# from aind_data_schema.core import rig
# from np_aind_metadata import utils


# rig_model = rig.Rig.model_validate_json(
#     Path("rig.json").read_text()
# )


# @pytest.mark.parametrize(
#     "model,filename",
#     [
#         (rig_model, Path("rig.json"), ),
#         (rig_model, Path("NP_rig.json"), ),
#         (rig_model, Path("NP__rig.json"), ),
#         (rig_model, Path("NP2_rig_20240401.json"), ),
#     ]
# )
# def test_save_aind_model_to_output_path(
#     model,
#     filename,
#     tmp_path,
# ) -> None:
#     output_path = tmp_path / filename
#     utils.save_aind_model_to_output_path(
#         model,
#         output_path,
#     )
#     assert output_path.exists(), "Output path should exist."
