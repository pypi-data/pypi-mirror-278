"""Vanilla algorithms test module"""

from src.pkg_support_resistance import VanillaSupportResistance
from src.pkg_support_resistance.data_set import sr_input_example
from .expected_output_test import vanilla_sr_exec_pipeline_expected_output_test


def test_vanilla_algorithms_exec_pipeline():
    """
    Test the calculation of support/resistance process.
    This test verifies that the function exec_pipeline,
    returns the expected output given a specific input file path and cluster threshold.
    """

    result: list[dict] = VanillaSupportResistance.exec_pipeline(
        input_data=sr_input_example, cluster_threshold=1
    )
    assert result == vanilla_sr_exec_pipeline_expected_output_test
